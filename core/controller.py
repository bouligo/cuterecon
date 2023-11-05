import re
import sys
import os

from PySide2.QtCore import QProcess, QModelIndex, QTimer
import html2text
import ipaddress  # sort by IP

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMessageBox, QInputDialog, QSystemTrayIcon

from core.config import Config
from utils.NmapParser import NmapParser
from core.view import View
from core.database import Database
from core.models.hostmodel import HostModel
from core.models.logmodel import LogModel
from core.models.jobmodel import JobModel


class Controller:
    APPLICATION_VERSION = "1.3"
    autosave_timer = QTimer()

    def __init__(self, ui):

        self.ui = ui
        self.view = View(ui, self)


        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(Config.get()['user_prefs']['autosave_interval'])

        self.setup_initial_project()

        if len(sys.argv) > 1:
            file_path = os.path.realpath(sys.argv[1])
            self.open_db(file_path)



    def setup_initial_project(self):
        Database.init_DB()
        self.setup_models()

        if Config.default_configuration_loaded:
            QMessageBox.information(None, 'No custom configuration found', 'QtRecon could not find your customized configuration file. Please copy the default example configuration file <i>config.json.example</i> to <i>config.json</i>, and edit its content to use your favorite tools !')
        binaries_issues = Config.check_binaries()
        for binary_not_found in binaries_issues['not_found']:
            self.log('RUNTIME', f"Binary {binary_not_found} cannot be found.")
        for binary_not_executable in binaries_issues['not_executable']:
            self.log('RUNTIME', f"Binary {binary_not_executable} is not executable.")

        self.log('RUNTIME', 'New project started ! Happy recon ;-)')
        self.ui.ui.actionAutosave_database_every_5_mins.setEnabled(False)
        Database.has_unsaved_data = False

    def setup_models(self):
        self.host_model = HostModel(self.ui, self)
        self.hosts_for_port_table = HostModel(self.ui, self)
        self.log_model = LogModel(self.ui)
        self.job_model = JobModel(self.ui, self)
        self.ui.ui.host_list.setModel(self.host_model) # LOL ?
        self.ui.ui.hosts_for_port_table.setModel(self.hosts_for_port_table)
        self.ui.ui.log_table.setModel(self.log_model)
        self.ui.ui.job_table.setModel(self.job_model)
        self.ui.ui.host_list.setColumnHidden(0, True)
        self.ui.ui.hosts_for_port_table.setColumnHidden(0, True)
        self.ui.ui.log_table.setColumnHidden(0, True)
        self.ui.ui.job_table.setColumnHidden(0, True)
        self.ui.ui.job_table.setColumnHidden(1, True)
        self.ui.ui.job_table.setColumnHidden(2, True)
        self.ui.ui.job_table.setColumnHidden(6, True)
        self.hosts_for_port_table.filter_hostlist('port', '')
        self.host_model.layoutChanged.emit()
        self.log_model.layoutChanged.emit()
        self.job_model.layoutChanged.emit()
        self.hosts_for_port_table.layoutChanged.emit()

    def save_conf(self):
        raise NotImplementedError

    def reload_conf(self):
        Config.load_config(False, True)
        self.view.setup_ui()
        self.ui.statusBar().showMessage('Reloaded configuration from disk !', 5000)

    def clear_db(self) -> bool:
        '''

        @return: agreement from user
        '''

        if Database.request("select count(id) from hosts").fetchone()['count(id)']:
            reply = QMessageBox.question(None, 'Confirmation', 'All unsaved data will be lost. Are you sure ?')

            if reply == QMessageBox.No:
                return False

        self.view.close_right_panel_tabs()
        self.job_model.kill_jobs()
        self.setup_initial_project()
        return True

    def autosave(self):
        if self.ui.ui.actionAutosave_database_every_5_mins.isChecked() and Database.current_savefile:
            self.save_db()

    def save_db(self, filename: str = ""):
        '''

        :param filename: (optionnal) if empty, tries to save to previous location
        :return: None
        '''
        if not filename:
            filename = Database.current_savefile

        exception = Database.export_DB(filename)
        if exception:
            QMessageBox.critical(None, 'Could not save current session', 'Exception occurred: ' + str(exception))
        else:
            self.log('RUNTIME', f"Saved current session to {filename}")
            self.ui.statusBar().showMessage('Saved database !', 15000)
            Database.has_unsaved_data = False
            self.ui.ui.actionAutosave_database_every_5_mins.setEnabled(True)

    def open_db(self, filename: str):
        if self.clear_db():
            exception = Database.import_DB(filename)

            if exception:
                QMessageBox.critical(None, 'Could not load session', 'Exception occurred: ' + str(exception))
            else:
                self.setup_models()
                self.host_model.update_data()
                self.hosts_for_port_table.update_data()
                self.update_hosts_for_port_panel()
                self.log_model.update_data()
                self.log('RUNTIME', f"Restored session {filename}")
                Database.has_unsaved_data = False
                self.ui.ui.actionAutosave_database_every_5_mins.setEnabled(True)

            self.ui.ui.host_list.clearSelection()
            self.log_model.layoutChanged.emit()

    def get_job(self, id: int) -> dict:
        return self.job_model.get_job(id)

    def get_selected_host(self, host: QModelIndex = None) -> dict:
        if not host and not self.host_model.itemData(self.ui.ui.host_list.currentIndex()):
            return ""

        if host:
            host_id = self.host_model.itemData(host)['id']
        elif self.host_model.itemData(self.ui.ui.host_list.currentIndex()):
            host_id =self.host_model.itemData(self.ui.ui.host_list.currentIndex())['id']

        return self.host_model.get_host_details(host_id)

    def get_selected_port(self) -> str:
        return self.view.app_tabs['Ports'].item(self.view.app_tabs['Ports'].currentRow(), 2).text()

    def set_host_pwned(self, index: QModelIndex):
        host = self.get_selected_host(index)
        self.host_model.set_host_pwned(host['id'])

    def set_host_highlight_color(self, index: QModelIndex, color: str):
        host = self.get_selected_host(index)
        self.host_model.set_host_highlight_color(host['id'], color)

    def change_host_hostname(self, index: QModelIndex, new_hostname: str):
        host = self.get_selected_host(index)
        self.host_model.change_host_hostname(host['id'], new_hostname)
        self.ui.ui.host_list.clearSelection()

    def change_host_os(self, index: QModelIndex, new_os: str):
        host = self.get_selected_host(index)
        self.host_model.change_host_os(host['id'], new_os.lower())
        self.ui.ui.host_list.clearSelection()

    def change_host_ip(self, index: QModelIndex, new_ip: str):
        host = self.get_selected_host(index)
        self.host_model.change_host_ip(host['id'], new_ip)
        self.ui.ui.host_list.clearSelection()

    def delete_host(self, index: QModelIndex):
        host = self.get_selected_host(index)
        self.host_model.delete_host(host['id'])

    def get_job_details(self, job: QModelIndex):
        return self.job_model.get_job_details(job)

    def update_notes_for_current_host(self, notes: str):
        host_id = self.get_selected_host()['id']
        self.host_model.update_notes_for_host(host_id, notes)

    def update_buttons(self):
        self.view.refresh_buttons()

    def update_right_panel(self):
        if self.host_model.itemData(self.ui.ui.host_list.currentIndex()):
            self.view.update_right_panel(self.ui.ui.host_list.currentIndex())

    def update_hosts_for_port_panel(self):
        ports_tcp = []
        ports_udp = []
        for host in self.host_model.get_all_host_details():
            for port in host['ports']:
                if port['proto'] == 'tcp':
                    ports_tcp.append(int(port['port']))
                elif port['proto'] == 'udp':
                    ports_udp.append(int(port['port']))

        unique_port_udp = sorted(list(dict.fromkeys(ports_udp)))
        unique_port_tcp = sorted(list(dict.fromkeys(ports_tcp)))
        self.view.update_hosts_for_port_panel({'udp':unique_port_udp, 'tcp':unique_port_tcp})

    # Todo: refactor
    def parse_nmap_xml(self, xml_file: str) -> int:
        '''

        @param xml_file: path to xml file to parse
        @return: new hosts and ports added to the database
        '''
        nmap_parser = NmapParser(xml_file)
        nmap_data = nmap_parser.parse_xml()
        new_hosts = self.host_model.update_hosts(nmap_data)

        if self.ui.ui.host_list.currentIndex().row() >= 0:
            self.view.update_right_panel(self.ui.ui.host_list.currentIndex())
        return new_hosts

    def parse_nmap_output(self, nmap_file: str):
        nmap_parser = NmapParser(nmap_file)
        nmap_output = nmap_parser.parse_nmap()
        self.host_model.update_nmap_output(nmap_output)

        if self.ui.ui.host_list.currentIndex().row() >= 0:
            self.view.update_right_panel(self.ui.ui.host_list.currentIndex())

    def filter_hostlist(self, search_input):
        self.ui.ui.host_list.clearSelection()
        self.view.close_right_panel_tabs()
        self.host_model.filter_hostlist('host', search_input)

    def filter_hosts_for_port_table(self, port: str):
        self.hosts_for_port_table.filter_hostlist('port', port)

    def autorun(self, hosts_ids: list):
        for host_id in hosts_ids:
            host_details = self.host_model.get_host_details(host_id)
            for port_details in host_details['ports']:
                for port in ['any', port_details['port']]:
                    if port_details['proto'] in Config.get()['autorun'] and port in Config.get()['autorun'][port_details['proto']]:
                        for program in Config.get()['autorun'][port_details['proto']][port]:
                            self.log('AUTORUN', f"Running {program} on {port_details['proto']}://{host_details['ip']}:{port}")
                            self.new_job(Config.get()['user_binaries'][program], host_details['id'], port)

    def log(self, category: str, data: str):
        if category not in ['RUNTIME', 'INFO', 'WARNING', 'CRITICAL', 'AUTORUN']:
            category = 'UNKNOWN'
        if category in ['CRITICAL', 'UNKNOWN']:
            QMessageBox.critical(None, 'Error', data)
        self.log_model.add_log([category, data])

    def search_string_in_db_hosts(self, search_term: str, ip: str = "") -> list:
        '''

        @param search_term: string to search
        @return: ['ip1', 'ip2'] or ['match1', 'match2']
        '''

        if ip:
            notes_sql = Database.request("select ip, notes from hosts where ip = ? and notes LIKE '%' || ? || '%'", (ip, search_term)).fetchone()
            notes = []
            if notes_sql:
                notes = ['Notes:']
                for line in html2text.html2text(notes_sql['notes']).split('\n'):
                    if search_term in line:
                        notes.append(line)
                notes.append("")

            tabs_sql = Database.request("select hosts_tabs.title, hosts_tabs.text from hosts, hosts_tabs where hosts.id = hosts_tabs.host_id and hosts.ip = ? and hosts_tabs.text LIKE '%' || ? || '%'", (ip, search_term)).fetchall()
            tabs = []
            for tab in tabs_sql:
                for line in html2text.html2text(tab['text']).split('\n'):
                    if search_term in line:
                        tabs.append(f"{tab['title']} : {line}")
            return notes + tabs # pas utile ?


        else:
            hosts_sql = Database.request("select distinct hosts.ip from hosts, hosts_tabs where hosts.id = hosts_tabs.host_id and (hosts_tabs.text LIKE '%' || ? || '%' OR hosts.notes LIKE '%' || ? || '%')", (search_term, search_term)).fetchall()
            return sorted(list(map(lambda host: host['ip'], hosts_sql)), key=ipaddress.IPv4Address)

    def remove_tab(self, tab: dict):
        if self.get_job(tab['job_id']):
            self.get_job(tab['job_id']).kill()
        self.host_model.remove_external_tab(tab['job_id'])

    def create_creds(self, host_id: str = "") -> int:
        host = self.host_model.get_host_details(host_id) if host_id else self.get_selected_host()
        return Database.request("INSERT INTO hosts_creds(host_id) VALUES (?) RETURNING id", (host['id'], )).fetchone()['id']

    def delete_creds(self, creds_ids: list) -> None:
        for cred_id in creds_ids:
            Database.request("DELETE FROM hosts_creds WHERE id = ?", (cred_id, ))

    def update_credentials(self, cred_id: str, column: str, new_value: str):
        Database.request(f"UPDATE hosts_creds SET {column} = ? WHERE id = ?", (new_value, cred_id))

    def new_job(self, program: dict, host_id: str = "", port: str = ""):
        host_dst = self.host_model.get_host_details(host_id) if host_id else self.get_selected_host()
        port_dst = port if port else self.get_selected_port()

        if 'args' in program:
            args = program['args'].copy()
            for i in range(len(program['args'])):
                args[i] = args[i].replace("%%%IP%%%", host_dst['ip'])
                args[i] = args[i].replace("%%%PORT%%%", port_dst)
                for variable in Config.get()['user_variables']:
                    if Config.get()['user_variables'][variable]:
                        args[i] = args[i].replace(f"%%%{variable}%%%", Config.get()['user_variables'][variable])

                uncaught_user_variables = re.findall('%{3}[a-zA-Z-_]+%{3}', args[i])
                if uncaught_user_variables:
                    for uncaught_user_variable in uncaught_user_variables:
                        reply = QInputDialog.getText(None, 'Unset variable', f"While trying to launch {program['name']} on {host_dst['ip']}:{port_dst}, the variable {uncaught_user_variable} was not set. You can specify it now:")
                        if reply[1]:
                            args[i] = args[i].replace(f"{uncaught_user_variable}", reply[0])
                        else:
                            args[i] = args[i].replace(f"{uncaught_user_variable}", "")

        else:
            args = []

        if 'working_directory' in program.keys() and program['working_directory']:
            working_directory = program['working_directory']
        else:
            working_directory = None

        if program['detached']:
            if 'in_terminal' in program.keys() and program['in_terminal']:
                args.insert(0, program['binary'])
                args = Config.get()['core_binaries']['terminal']['args'] + args
                self.start_detached_job(Config.get()['core_binaries']['terminal']['binary'], args, working_directory)
            else:
                self.start_detached_job(program['binary'], args, working_directory)
        else:
            job_id = self.start_attached_job(program['binary'], args, working_directory, host_dst['ip'])
            self.host_model.create_external_tab(host_dst['id'], program['name'], job_id)
            if self.get_selected_host():
                if host_dst and self.get_selected_host()['ip'] == host_dst['ip']:
                    self.view.new_tab(program['name'], job_id, "") # "" ?

    def kill_job(self, job_id: int):
        self.job_model.get_job(job_id).kill()

    def pause_job(self, job_id: int):
        self.job_model.get_job(job_id).pause()

    def resume_job(self, job_id: int):
        self.job_model.get_job(job_id).resume()

    def new_scan(self, target: str, speed: str, ports: str, skip_host_discovery: bool, version_probing: bool, default_scripts: bool, os_detection: bool, tcp_and_udp: bool):
        self.log('INFO', 'Starting new scan on ' + target)
        self.job_model.new_scan(target, speed, ports, skip_host_discovery, version_probing, default_scripts, os_detection, tcp_and_udp)

    def start_attached_job(self, command: str, args: list, working_directory: str, host_id: int) -> int:
        self.log('INFO', f"Starting new job ({command} {' '.join(args)})")
        return self.job_model.new_attached_job(command, args, working_directory, host_id)

    def start_detached_job(self, command: str, args: list, working_directory: str):
        # External program
        self.log('INFO', f"Launching external program {command} {' '.join(args)}")
        job = QProcess()
        job.setWorkingDirectory(working_directory)
        success = job.startDetached(command, args)
        if not success:
            self.log("CRITICAL", "Cannot launch program " + command)

    def send_desktop_notification(self, title: str, message: str):
        system_icon = QSystemTrayIcon()
        system_icon.setIcon(QIcon("icons/icon.ico"))
        system_icon.setVisible(True)
        system_icon.showMessage(title, message, msecs=10000)
        system_icon.setVisible(False)