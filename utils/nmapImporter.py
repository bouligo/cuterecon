import multiprocessing
import queue
import time

from PySide6.QtCore import QThread, Signal, QObject, Qt
from PySide6.QtWidgets import QWidget, QProgressDialog

from core.database import Database
from ui.replace_host_data import Replace_host_data
from utils.NmapParser import NmapParser


def job_parse_xml_file(input_file):
    nmap_parser = NmapParser(input_file)
    return nmap_parser.parse_xml()


class Thread_import_xml_nmap(QObject):
    status = Signal(str)
    parser_progression = Signal(int, int)
    database_progression = Signal(int, int)
    ask_user_what_to_do = Signal(str, str)
    finished = Signal()

    def __init__(self, parent, input_data, queue: queue.Queue):
        self.parent = parent
        self.nmap_data = {}
        self.input_data = input_data
        self.returning_host_ids = {}
        self.stop_requested = False
        self.user_answers = queue
        super().__init__()

    def stop(self):
        self.stop_requested = True

    def import_xml_files(self):
        nb_of_processes = max(multiprocessing.cpu_count()-1, 1)
        pool = multiprocessing.Pool(processes=nb_of_processes)
        results = []

        for i in range(len(self.input_data)):  # One "job" per file
            results.append(pool.map_async(job_parse_xml_file, [self.input_data[i]]))

        while True:
            if self.stop_requested:
                pool.terminate()
                return
            number_of_jobs_finished = sum([result.ready() for result in results])
            self.parser_progression.emit(number_of_jobs_finished, len(self.input_data))
            self.status.emit(f"Step 1/2 : parsing XML files ({number_of_jobs_finished}/{len(self.input_data)})")
            if all([result.ready() for result in results]):
                break
            time.sleep(1)

        pool.close()
        pool.join()
        for result in results:
            self.nmap_data.update(result.get()[0])

        self.status.emit(f"Step 2/2 : Importing {len(self.nmap_data)} hosts into database ...")
        do_not_prompt_user_anymore = False
        for i, host in enumerate(self.nmap_data.keys()):
            if not self.stop_requested:
                # Check if IP is already in database
                id_of_already_existing_machine = Database.request("SELECT id FROM hosts WHERE ip = ?", (self.nmap_data[host]['ip'], )).fetchone()
                if id_of_already_existing_machine:
                    if not do_not_prompt_user_anymore:
                        self.ask_user_what_to_do.emit(self.nmap_data[host]['ip'], "" or self.nmap_data[host]['hostname'])
                        response, dialog_box = self.user_answers.get()

                    if response == dialog_box.ui.merge_all:
                        do_not_prompt_user_anymore = True
                        response = dialog_box.ui.merge
                    if response == dialog_box.ui.merge:
                        sqlite_cursor = Database.request("UPDATE hosts SET hostname = ?, mac = ?, os = ? where ip = ? RETURNING id",(self.nmap_data[host]['hostname'], self.nmap_data[host]['mac'], self.nmap_data[host]['os'], self.nmap_data[host]['ip']))
                        host_id = sqlite_cursor.fetchone()['id']
                        old_hosts_ports = Database.request("SELECT port, proto FROM hosts_ports WHERE host_id = ?", (host_id, )).fetchall()
                        old_data = {}
                        old_data['tcp'] = [i['port'] for i in old_hosts_ports if i['proto'] == 'tcp']
                        old_data['udp'] = [i['port'] for i in old_hosts_ports if i['proto'] == 'udp']

                        for proto in ['tcp', 'udp']:
                            for port in self.nmap_data[host]['ports'][proto].keys():
                                if port in old_data[proto]:
                                    Database.request("UPDATE hosts_ports SET description = ? WHERE host_id = ? AND proto = ? AND port = ?", (self.nmap_data[host]['ports'][proto][port]['description'], host_id, proto, port))
                                else:
                                    Database.request("INSERT INTO hosts_ports(host_id, proto, port, status, description) VALUES (?, ?, ?, ?, ?)", (host_id, proto, port, self.nmap_data[host]['ports'][proto][port]['status'], self.nmap_data[host]['ports'][proto][port]['description']))
                                    if host_id not in self.returning_host_ids.keys():
                                        self.returning_host_ids[host_id] = {'tcp': [], 'udp': []}
                                    self.returning_host_ids[host_id][proto].append(port)

                    if response == dialog_box.ui.erase_all:
                        do_not_prompt_user_anymore = True
                        response = dialog_box.ui.erase

                    if response == dialog_box.ui.keep_all:
                        do_not_prompt_user_anymore = True
                        response = dialog_box.ui.keep
                    if response == dialog_box.ui.keep:
                        continue

                if not id_of_already_existing_machine or response == dialog_box.ui.erase:  # Host is not already in database
                    sqlite_cursor = Database.request("INSERT INTO hosts(os, ip, hostname, mac, pwned) values(?, ?, ?, ?, 0) ON CONFLICT(ip) DO UPDATE SET hostname = ?, mac = ?, os = ? where ip = ? RETURNING id", (self.nmap_data[host]['os'],  self.nmap_data[host]['ip'],  self.nmap_data[host]['hostname'],  self.nmap_data[host]['mac'],  self.nmap_data[host]['hostname'],  self.nmap_data[host]['mac'], self.nmap_data[host]['os'], self.nmap_data[host]['ip']))
                    host_id = sqlite_cursor.fetchone()['id']
                    Database.request('delete from hosts_ports where host_id = ?', (host_id,))
                    self.returning_host_ids[host_id] = {'tcp': [], 'udp': []}

                    for proto in ['udp', 'tcp']:
                        for port in self.nmap_data[host]['ports'][proto]:
                            Database.request("insert into hosts_ports(host_id, proto, port, status, description) values(?, ?, ?, ?, ?)", (host_id, proto, port,  self.nmap_data[host]['ports'][proto][port]['status'], self.nmap_data[host]['ports'][proto][port]['description']))
                    self.database_progression.emit(i+1, len(self.nmap_data.keys()))

        self.status.emit(f"Finalizing ...")
        self.finished.emit()


class ProgressBar_import_hosts():  # https://stackoverflow.com/questions/47156183/qprogressdialog-only-shows-after-long-running-code-is-finished/47166811#47166811
    def __init__(self, caller, is_displayed: bool, data):
        super().__init__()
        self.caller = caller
        self.is_displayed = is_displayed
        self.queue = queue.Queue()
        self.worker = Thread_import_xml_nmap(caller.ui, data, self.queue)
        self.worker.ask_user_what_to_do.connect(self.ask_user_what_to_do)

        if self.is_displayed:
            self.thread = QThread()
            self.worker.moveToThread(self.thread)
            self.worker.finished.connect(self.thread.quit)
            self.thread.started.connect(self.worker.import_xml_files)
            self.thread.finished.connect(self.worker.deleteLater)

            self.progress = QProgressDialog(self.caller.ui)
            self.progress.setWindowTitle("Importing XML files")
            self.progress.setAutoClose(False)
            self.progress.setFixedSize(600, 100)
            self.progress.setWindowModality(Qt.ApplicationModal)
            self.progress.canceled.connect(self.worker.stop, type=Qt.DirectConnection)
            self.worker.parser_progression.connect(self.updateProgress)
            self.worker.database_progression.connect(self.updateProgress)
            self.worker.status.connect(self.updateStatus)
            self.thread.finished.connect(lambda: self.caller.finished_parse_nmap_data(self, self.worker.returning_host_ids))
            self.thread.finished.connect(self.progress.close)
            self.progress.forceShow()
            self.thread.start()
        else:
            self.worker.import_xml_files()

    def updateStatus(self, text):
        self.progress.setLabelText(text)

    def updateProgress(self, value, maximum):
        if not self.progress.wasCanceled():
            self.progress.setValue(value)
            self.progress.setMaximum(maximum)

    def ask_user_what_to_do(self, ip: str, hostname: str):
        dialog_box = Replace_host_data(self.progress if self.is_displayed else self.caller.ui, ip, hostname)
        self.queue.put([dialog_box.exec(), dialog_box])