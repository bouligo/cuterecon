import multiprocessing
import time

from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel

from core.database import Database
from utils.NmapParser import NmapParser


def job_parse_xml_file(input_file):
    nmap_parser = NmapParser(input_file)
    return nmap_parser.parse_xml()

class Thread_import_xml_nmap(QObject):
    status = Signal(str)
    parser_progression = Signal(int, int)
    database_progression = Signal(int, int)
    finished = Signal()

    def __init__(self, input_data):
        self.nmap_data = {}
        self.input_data = input_data
        self.returning_host_ids = []
        self.stop_requested = False
        super().__init__()

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
            self.status.emit(f"Parsing XML files ({number_of_jobs_finished}/{len(self.input_data)})")
            if all([result.ready() for result in results]):
                break
            time.sleep(1)

        pool.close()
        pool.join()
        for result in results:
            self.nmap_data.update(result.get()[0])

        self.status.emit(f"Importing {len(self.nmap_data)} hosts into database ...")
        for i, host in enumerate(self.nmap_data.keys()):
            if not self.stop_requested:
                sqlite_cursor = Database.request(" INSERT INTO hosts(os, ip, hostname, mac, pwned) values(?, ?, ?, ?, 0) ON CONFLICT(ip) DO UPDATE SET hostname = ?, mac = ?, os = ? where ip = ? RETURNING id", (self.nmap_data[host]['os'],  self.nmap_data[host]['ip'],  self.nmap_data[host]['hostname'],  self.nmap_data[host]['mac'],  self.nmap_data[host]['hostname'],  self.nmap_data[host]['mac'], self.nmap_data[host]['os'], self.nmap_data[host]['ip']))
                host_id = sqlite_cursor.fetchone()['id']
                Database.request('delete from hosts_ports where host_id = ?', (host_id,))
                self.returning_host_ids.append(host_id)

                for proto in ['udp', 'tcp']:
                    for port in self.nmap_data[host]['ports'][proto]:
                        Database.request("insert into hosts_ports(host_id, proto, port, status, description) values(?, ?, ?, ?, ?)", (host_id, proto, port,  self.nmap_data[host]['ports'][proto][port]['status'], self.nmap_data[host]['ports'][proto][port]['description']))
                self.database_progression.emit(i+1, len(self.nmap_data.keys()))

        self.status.emit(f"Finalizing ...")
        self.finished.emit()

class ProgressBar_update_hosts(QWidget):
    def closeEvent(self, event):
        self.worker.stop_requested = True
        self.thread.quit()

    def __init__(self, caller, data):
        super().__init__()
        self.caller = caller
        self.progressbar_parser = QProgressBar(self)
        self.progressbar_parser.setGeometry(0, 0, 400, 80)
        self.progressbar_database = QProgressBar(self)
        self.progressbar_database.setGeometry(0, 0, 400, 80)
        self.label = QLabel()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progressbar_parser)
        self.layout.addWidget(self.progressbar_database)
        self.setLayout(self.layout)
        self.setGeometry(0, 0, 600, 100)
        self.setWindowTitle('Importing Nmap data')

        self.worker = Thread_import_xml_nmap(data)
        self.thread = QThread()
        self.worker.status.connect(self.change_status)
        self.worker.parser_progression.connect(self.set_parser_progression)
        self.worker.database_progression.connect(self.set_database_progression)
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.thread.quit)
        self.thread.started.connect(self.worker.import_xml_files)
        self.thread.finished.connect(lambda: self.caller.finished_parse_nmap_data(self.worker.returning_host_ids))
        self.thread.finished.connect(self.close)
        self.thread.start()

    def set_parser_progression(self, value, maximum):
        self.progressbar_parser.setMaximum(maximum)
        self.progressbar_parser.setValue(value)

    def set_database_progression(self, value, maximum):
        self.progressbar_database.setMaximum(maximum)
        self.progressbar_database.setValue(value)

    def change_status(self, text):
        self.label.setText(text)
