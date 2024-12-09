import os
import sys

from PySide6.QtCore import QAbstractTableModel, Qt, Signal
import ipaddress  # sort by IP

from PySide6.QtGui import QFont, QColor, QIcon

from core.database import Database


class HostModel(QAbstractTableModel):
    data_updated = Signal(int, int)  # Displayed number of hosts / all hosts

    def __init__(self, parent, controller):
        QAbstractTableModel.__init__(self, parent)
        self.controller = controller
        self.hosts = []
        self.headers = ['host_id', 'OS', 'IP', 'Hostname']
        self.os = {'linux': QIcon(os.path.abspath(os.path.dirname(sys.argv[0])) + "/icons/linux.png"), 'windows': QIcon(os.path.abspath(os.path.dirname(sys.argv[0])) + "/icons/windows.png"), 'ios': QIcon(os.path.abspath(os.path.dirname(sys.argv[0])) + "/icons/ios.png"), 'unknown': QIcon(os.path.abspath(os.path.dirname(sys.argv[0])) + "/icons/unknown.png")}
        self.filter = ""
        self.filter_type = "host"

    def update_data(self):
        hosts = []
        if self.filter_type == 'host':
            all_hosts = Database.request("SELECT id as host_id, os, ip, hostname, pwned, highlight FROM hosts").fetchall()
            hosts = Database.request("SELECT id as host_id, os, ip, hostname, pwned, highlight FROM hosts WHERE ip LIKE '%' || ? || '%' OR hostname LIKE '%' || ? || '%'",(self.filter, self.filter)).fetchall()
            self.data_updated.emit(len(hosts), len(all_hosts))
        elif self.filter_type == 'port' and '/' in self.filter:
            proto, port = self.filter.split('/')
            hosts = Database.request("SELECT id as host_id, os, ip, hostname, pwned, highlight FROM hosts, hosts_ports WHERE hosts.id = hosts_ports.host_id AND hosts_ports.proto = ? AND hosts_ports.port = ?", (proto, port)).fetchall()

        self.hosts = sorted(hosts, key=lambda d: ipaddress.IPv4Address(d['ip']))
        self.layoutChanged.emit()  # https://stackoverflow.com/questions/45359569/how-to-update-qtableview-on-qabstracttablemodel-change

    def headerData(self, col, orientation, role):
        # if role == Qt.TextAlignmentRole:
        #     return Qt.AlignCenter # BUG: RuntimeWarning: libshiboken: Overflow: Value PySide6.QtCore.Qt.AlignmentFlag.AlignCenter exceeds limits of type  [signed] "i" (4bytes).
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[col]
        return None

    def rowCount(self, parent):
        return len(self.hosts)

    def columnCount(self, parent):
        return len(self.headers)

    def itemData(self, index):
        if index.row() >= 0:
            return self.hosts[index.row()]

    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid():
            return None
        elif role == Qt.FontRole:
            if self.hosts[index.row()]['pwned']:
                validated = QFont()
                validated.setItalic(True)
                validated.setStrikeOut(True)
                return validated
        elif role == Qt.BackgroundRole:
            if self.hosts[index.row()]['highlight']:
                try:
                    return QColor(getattr(Qt, self.hosts[index.row()]['highlight']))
                except AttributeError:
                    self.controller.log("RUNTIME", f"{self.hosts[index.row()]['highlight']} is not valid")
        if role == Qt.DecorationRole:
            if index.column() == 1:
                try:
                    return self.os[self.hosts[index.row()]['os'].lower()]
                except KeyError:  # Unknown OS from self.os
                    return self.os['unknown']
                except AttributeError:  #Null value in DB
                    return self.os['unknown']

        if role == Qt.DisplayRole:
            if index.column() == 0:  # This is a hidden column
                return self.hosts[index.row()]['host_id']
            if index.column() == 2:
                return self.hosts[index.row()]['ip']
            if index.column() == 3:
                return self.hosts[index.row()]['hostname']

    def filter_hostlist(self, filter_type: str, search_input: str):
        self.filter_type = filter_type
        self.filter = search_input
        self.update_data()

    def update_notes_for_host(self, host_id: int, notes: str):
        Database.request("update hosts set notes = ? where id = ?", (notes, host_id))

    def update_nmap_output(self, hosts: dict):
        for host in hosts:
            Database.request("update hosts set nmap = ? where ip = ?", (hosts[host], host))

    def change_host_ip(self, host_id: int, new_ip: str):
        Database.request("update hosts set ip = ? where id = ?", (new_ip, host_id))
        self.update_data()

    def change_host_hostname(self, host_id: int, new_hostname: str):
        Database.request("update hosts set hostname = ? where id = ?", (new_hostname, host_id))
        self.update_data()

    def change_host_os(self, host_id: int, new_os: str):
        Database.request("update hosts set os = ? where id = ?", (new_os, host_id))
        self.update_data()

    def set_host_pwned(self, host_id: int):
        Database.request("update hosts set pwned = (1 - (pwned & 1)) where id = ?", (host_id,))
        self.update_data()

    def set_host_highlight_color(self, host_id: int, color: str):
        if color:
            Database.request("update hosts set highlight = ? where id = ?", (color, host_id))
        else:
            Database.request("update hosts set highlight = NULL where id = ?", (host_id,))
        self.update_data()

    def create_external_tab(self, host_id: int, app_name: str, cmdline: str, job_id: int):
        Database.request("insert into hosts_tabs(host_id, job_id, cmdline, title) values(?, ?, ?, ?)", (host_id, job_id, cmdline, app_name))

        job = self.controller.get_job(job_id)

        self.update_external_tab(job_id, job.output_text)
        job.readyReadStandardOutput.connect(
            lambda: self.update_external_tab(job_id, job.output_text))
        job.readyReadStandardError.connect(
            lambda: self.update_external_tab(job_id, job.output_text))

    def remove_external_tab(self, job_id: int):
        Database.request('delete from hosts_tabs where job_id = ?', (job_id, ))

    def update_external_tab(self, job_id: int, text: str):
        Database.request('update hosts_tabs set text = ? where job_id = ?', (text, job_id))

    def get_host_details(self, host_id: int):
        host = Database.request('select * from hosts where id = ?', (host_id, )).fetchone()
        host['ports'] = Database.request('select * from hosts_ports where host_id = ?', (host_id, )).fetchall()
        host['external_tabs'] = Database.request('select * from hosts_tabs where host_id = ?', (host_id, )).fetchall()
        host['credentials'] = Database.request('select * from hosts_creds where host_id = ?', (host_id, )).fetchall()
        return host

    def delete_host(self, host_id: int):
        Database.request('delete from hosts_ports where host_id = ?', (host_id,))
        Database.request('delete from hosts_tabs where host_id = ?', (host_id,))
        Database.request('delete from hosts where id = ?', (host_id,))
        self.update_data()

    def delete_hosts_with_no_services(self):
        Database.request('DELETE FROM hosts WHERE id NOT IN (SELECT host_id from hosts_ports);')
        self.update_data()