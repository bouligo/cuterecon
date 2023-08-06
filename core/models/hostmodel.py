from PySide2.QtCore import QAbstractTableModel, Qt
import ipaddress  # sort by IP

from PySide2.QtGui import QFont, QColor, QIcon

from core.database import Database


class HostModel(QAbstractTableModel):
    def __init__(self, parent, controller):
        QAbstractTableModel.__init__(self, parent)
        self.controller = controller
        self.hosts = []
        self.headers = ['id', 'OS', 'IP', 'Hostname']
        self.os = {'linux': QIcon("icons/linux.png"), 'windows': QIcon("icons/windows.png"), 'unknown': QIcon("icons/unknown.png")}
        self.filter = ""
        self.filter_type = "host"

    def update_data(self):
        if self.filter_type == 'host':
            hosts = Database.request("SELECT id, os, ip, hostname, pwned, highlight FROM hosts WHERE ip LIKE '%' || ? || '%' OR hostname LIKE '%' || ? || '%'", (self.filter, self.filter)).fetchall()
            self.hosts = sorted(hosts, key=lambda d: ipaddress.IPv4Address(d['ip']))
        elif self.filter_type == 'port':
            hosts = Database.request("SELECT hosts.* FROM hosts, hosts_ports WHERE hosts.id = hosts_ports.host_id AND hosts_ports.port = ?", (self.filter, )).fetchall()
            self.hosts = sorted(hosts, key=lambda d: ipaddress.IPv4Address(d['ip']))

    def headerData(self, col, orientation, role):
        # if role == Qt.TextAlignmentRole:
        #     return Qt.AlignCenter # BUG: RuntimeWarning: libshiboken: Overflow: Value PySide2.QtCore.Qt.AlignmentFlag.AlignCenter exceeds limits of type  [signed] "i" (4bytes).
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[col]
        return None

    def rowCount(self, parent):
        return len(self.hosts)

    def columnCount(self, parent):
        return len(self.headers)

    def itemData(self, index):
        return self.hosts[index.row()]

    def data(self, index, role):
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
                    print("Failed")
        if role == Qt.DecorationRole:
            if index.column() == 1:
                try:
                    return self.os[self.hosts[index.row()]['os'].lower()]
                except KeyError: # Unknown OS from self.os
                    return self.os['unknown']
                except AttributeError: #Null value in DB
                    return self.os['unknown']

        if role == Qt.DisplayRole:
            if index.column() == 0: # This is a hidden column
                return self.hosts[index.row()]['id']
            if index.column() == 2:
                return self.hosts[index.row()]['ip']
            if index.column() == 3:
                return self.hosts[index.row()]['hostname']

    def filter_hostlist(self, filter_type: str, search_input: str):
        self.filter_type = filter_type
        self.filter = search_input
        self.update_data()
        self.layoutChanged.emit()  # https://stackoverflow.com/questions/45359569/how-to-update-qtableview-on-qabstracttablemodel-change

    def update_hosts(self, hosts: dict) -> list:
        '''

        @param hosts: result from nmap_parser {'10.x.x.x': {'ip': '10.x.x.x, 'hostname': 'x', 'mac': '00:11:22:33:44:55', 'ports': {'tcp': {'53': {'status': 'open', 'description': 'dnsmasq UNKNOWN'}}, 'udp': {}}}
        @return: array containing new hosts id's
        '''
        known_ips = [i['ip'] for i in Database.request("select distinct(ip) from hosts").fetchall()]
        returning_host_ids = []
        for host in hosts.keys():
            if host not in known_ips:
                sqlite_cursor = Database.request("insert into hosts(os, ip, hostname, mac, pwned) values(?, ?, ?, ?, 0)", (hosts[host]['os'], hosts[host]['ip'], hosts[host]['hostname'], hosts[host]['mac']))
                host_id = sqlite_cursor.lastrowid
                returning_host_ids.append(host_id)
            else:
                sqlite_cursor = Database.request('update hosts set hostname = ?, mac = ?, os = ? where ip = ? returning id', (hosts[host]['hostname'], hosts[host]['mac'], hosts[host]['os'], hosts[host]['ip']))
                host_id = sqlite_cursor.fetchone()['id']
                returning_host_ids.append(host_id)
                Database.request('delete from hosts_ports where host_id = ?', (host_id,))

            for proto in ['udp', 'tcp']:
                for port in hosts[host]['ports'][proto]:
                    Database.request("insert into hosts_ports(host_id, proto, port, status, description) values(?, ?, ?, ?, ?)",
                                     (host_id, proto, port, hosts[host]['ports'][proto][port]['status'], hosts[host]['ports'][proto][port]['description']))

        self.update_data()
        self.layoutChanged.emit()  # https://stackoverflow.com/questions/45359569/how-to-update-qtableview-on-qabstracttablemodel-change
        return returning_host_ids

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

    def create_external_tab(self, host_id: int, app_name: str, job_id: int):
        Database.request("insert into hosts_tabs(host_id, job_id, title) values(?, ?, ?)", (host_id, job_id, app_name))

        job = self.controller.get_job(job_id)

        self.update_external_tab(job_id, job.get_output_text())
        job.readyReadStandardOutput.connect(
            lambda: self.update_external_tab(job_id, job.get_output_text()))
        job.readyReadStandardError.connect(
            lambda: self.update_external_tab(job_id, job.get_output_text()))

    def remove_external_tab(self, job_id: int):
        Database.request('delete from hosts_tabs where job_id = ?', (job_id, ))

    def update_external_tab(self, job_id: int, text: str):
        Database.request('update hosts_tabs set text = ? where job_id = ?', (text, job_id))

    def get_host_details(self, host_id: int):
        host = Database.request('select * from hosts where id = ?', (host_id, )).fetchone()
        host['ports'] = Database.request('select * from hosts_ports where host_id = ?', (host_id, )).fetchall()
        host['external_tabs'] = Database.request('select * from hosts_tabs where host_id = ?', (host_id, )).fetchall()
        return host

    def get_all_host_details(self):
        res = []
        for host in self.hosts:
            res.append(self.get_host_details(host['id']))
        return res

    def delete_host(self, host_id: int):
        Database.request('delete from hosts_ports where host_id = ?', (host_id,))
        Database.request('delete from hosts_tabs where host_id = ?', (host_id,))
        Database.request('delete from hosts where id = ?', (host_id,))
        self.update_data()
