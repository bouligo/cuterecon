import os
import shlex

from PySide6.QtCore import QAbstractTableModel, Qt, QProcess, QModelIndex, QProcessEnvironment
from datetime import datetime
from core.database import Database

from core.config import Config
from utils.job import Job, JobType


class JobModel(QAbstractTableModel):
    def __init__(self, parent, controller):
        QAbstractTableModel.__init__(self, parent)
        self.ui = parent
        self.controller = controller
        self.jobs = []
        self.jobs_objects = dict() # {(int) job_id: (Job) job }
        self.headers = ['id', 'host_id', 'type', 'timestamp', 'state', 'command', 'job']
        self.nmap_output_folder = Config.config['paths']['nmap_output_dir'] + '/' + str(datetime.timestamp(datetime.now()))

        # Create directory for nmap outputs
        if not os.access(self.nmap_output_folder, os.F_OK):  # Check for existence
            os.mkdir(self.nmap_output_folder)

    def update_data(self):
        self.jobs = Database.request("select * from jobs order by id ASC").fetchall()

    def rowCount(self, parent):
        return len(self.jobs_objects)

    def columnCount(self, parent):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None

        if index.column() == 3:
            return datetime.fromtimestamp(self.jobs[index.row()][self.headers[index.column()]]).isoformat(' ', timespec='seconds')
        if index.column() == 6:
            return self.jobs_objects[self.jobs]
        else:
            return self.jobs[index.row()][self.headers[index.column()]]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == 3:
                return 'Date'
            if col == 4:
                return 'Status ($?)'
            if col == 5:
                return 'Command'
        return None

    # def sort(self, col, order):
    #     self.layoutAboutToBeChanged.emit()
    #     self.jobs = sorted(self.jobs, key=operator.itemgetter(col))
    #     if order == Qt.DescendingOrder:
    #         self.jobs.reverse()
    #     self.layoutChanged.emit()

    def emit_refresh(self):
        self.layoutChanged.emit()  # https://stackoverflow.com/questions/45359569/how-to-update-qtableview-on-qabstracttablemodel-change
        self.ui.ui.job_table.resizeColumnsToContents()
        self.controller.update_buttons()

    def kill_jobs(self):
        for i in self.jobs_objects:
            self.jobs_objects[i].kill()
            self.jobs_objects[i].waitForFinished()

    def get_job_details(self, index: QModelIndex):
        return self.jobs[index.row()]

    def get_job(self, job_id: int) -> Job or None:
        if job_id in self.jobs_objects.keys():
            return self.jobs_objects[job_id]
        return None

    def add_job(self, job_type: JobType, privileged: bool, command: str, args: list, working_directory: str, host_id: int) -> int:
        if host_id:
            sqlite_cursor = Database.request("insert into jobs(host_id, type, timestamp) values(?, ?, ?)",
                (host_id, job_type.value, datetime.now().timestamp()))
        else:
            sqlite_cursor = Database.request("insert into jobs(type, timestamp) values(?, ?)",
                (job_type.value, datetime.now().timestamp()))

        job_id = sqlite_cursor.lastrowid

        if job_type == JobType.SCAN:
            arg_nmap_output = ['-oX', f"{self.nmap_output_folder}/scan-{job_id}.xml",
                     '-oN', f"{self.nmap_output_folder}/scan-{job_id}.nmap"]
            args = arg_nmap_output + args

        if privileged and Config.get()['core_binaries']['graphical_su']['binary']:  # needs root
            args.insert(0, command)
            if Config.get()['core_binaries']['graphical_su']['args']:
                args = Config.get()['core_binaries']['graphical_su']['args'] + args
            command = Config.get()['core_binaries']['graphical_su']['binary']

        job = Job()
        env = QProcessEnvironment.systemEnvironment()
        env.remove("VIRTUAL_ENV")
        job.setProcessEnvironment(env)
        if working_directory:
            job.setWorkingDirectory(working_directory)

        self.jobs_objects[job_id] = job

        Database.request("update jobs set state = ?, command = ? where id = ?",
                       (str(job.state()).split('.')[-1], command + ' ' + ' '.join(args), job_id))

        job.finished.connect(lambda ret_code, exit_status: self.job_is_finished(job_id, ret_code, exit_status))  # Needing lambda to give identifier
        job.stateChanged.connect(lambda new_state: self.update_job_state(job_id, new_state))  # Needing lambda to give identifier
        job.errorOccurred.connect(lambda error: self.job_crashed(job_id, error))  # Needing lambda to give identifier
        if Config.get()['user_prefs']['dev_null_as_stdin']:
            job.setStandardInputFile(QProcess.nullDevice())
        job.start(command, args)
        self.emit_refresh()
        self.update_data()
        return job_id

    def update_job_state(self, identifier: int, new_state: QProcess.ProcessState):
        # {0: 'Not running', 1: 'Starting', 2: 'Running'}
        Database.request("update jobs set state = ? where id = ?",
                         (str(new_state).split('.')[-1], identifier))
        # self.jobs[identifier]['state'] = str(new_state).split('.')[-1]
        self.update_data()
        self.emit_refresh()

    def job_crashed(self, identifier: int, error: QProcess.ProcessError):
        # {0: 'FailedToStart', 1: 'Crashed', 2: 'Timedout', 3: 'WriteError', 4: 'ReadError', 5: 'UnknownError'}
        error_short = str(error).split('.')[-1]
        current_job = Database.request("select command from jobs where id = ?", (identifier,)).fetchone()
        self.controller.log('WARNING', f"{current_job['command']} {error_short}")
        self.update_data()
        self.emit_refresh()

    def job_is_finished(self, identifier, ret_code, exit_status):
        # {0: 'NormalExit', 1: 'CrashExit'}
        if exit_status == QProcess.ExitStatus.NormalExit:
            status = "Success"
        else:
            status = "Crashed"

        Database.request("update jobs set state = ? where id = ?",
                         (f"{status} ({str(ret_code)})", identifier))
        self.update_data()
        self.emit_refresh()

        current_job = Database.request("select type from jobs where id = ?",
                                       (identifier,)).fetchone()
        if current_job['type'] == JobType.SCAN.value:
            xml_file = f"{self.nmap_output_folder}/scan-{identifier}.xml"
            nmap_file = f"{self.nmap_output_folder}/scan-{identifier}.nmap"

            if status == "Success" and ret_code == 0:
                self.controller.send_desktop_notification('Scan finished', 'Nmap scan finished successfully !')
                self.controller.start_parse_nmap_data(self, 'xml', [xml_file])
                self.controller.start_parse_nmap_data(self, 'nmap', nmap_file)
                self.controller.update_right_panel()
                self.controller.update_hosts_for_port_panel()
            else:
                self.controller.send_desktop_notification('Scan crashed', "An error occurred during the scan")
                self.controller.log('CRITICAL', f"Failed nmap scan: {self.jobs_objects[identifier].get_stderr_only()}")

            if Config.get()['user_prefs']['remove_nmap_xml_files_after_scan']:
                os.remove(xml_file)
                os.remove(nmap_file)

    def new_scan(self, target: str, ports: str, type: str, speed: str, additional_args: str, skip_host_discovery: bool, version_probing: bool, default_scripts: bool, os_detection: bool, tcp_and_udp: bool):
        command_from_conf = Config.get()['core_binaries']['nmap']['binary']
        args_from_conf = Config.get()['core_binaries']['nmap']['args']

        args = [speed]

        args.append(type)
        if tcp_and_udp:
            args.append('-sU')
        if version_probing:
            args.append('-sV')
        if default_scripts:
            args.append('-sC')
        if skip_host_discovery:
            args.append('-Pn')
        if os_detection:
            args.append('-O')
        if ports:
            args.append(f"-p{ports}")
        if additional_args:
            args += shlex.split(additional_args)
        args.append(target)

        privileged_scan_types = ['-sS', '-sA', '-sW', '-sM', '-sN', '-sF', 'sX']
        self.add_job(JobType.SCAN, os_detection or type in privileged_scan_types or '-sU' in args, command_from_conf, args_from_conf + args, "", "")

    def new_attached_job(self, command: str, args: list, working_directory: str, host_id: int) -> int:
        # Tabbed program
        return self.add_job(JobType.ATTACHED_PROGRAM, False, command, args, working_directory, host_id) # TODO: hardcoded False for non-privileged process

    def new_detached_job(self, command: str, args: list):
        # External program
        QProcess().startDetached(command, args)
