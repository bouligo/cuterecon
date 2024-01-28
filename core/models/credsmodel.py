import operator

from PySide6.QtCore import QAbstractTableModel, Qt
from core.database import Database


class CredsModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.ui = parent
        self.creds = []
        self.filter = ""
        self.sort_field = "hosts_creds.id"
        self.sort_order = "ASC"
        self.headers = ['host_id', 'id', 'IP', 'Hostname', 'Type', 'Domain', 'Username', 'Password'] # Must be the same as column names in db, but exception for host_id

    def update_data(self):
        if self.filter:
            self.creds = Database.request(f"SELECT hosts.id as host_id, hosts_creds.id, hosts.ip, hosts.hostname, hosts_creds.type, hosts_creds.domain, hosts_creds.username, hosts_creds.password FROM hosts, hosts_creds WHERE hosts.id == hosts_creds.host_id AND (hosts.hostname LIKE '%' || ? || '%' OR hosts_creds.domain LIKE '%' || ? || '%' OR hosts_creds.username LIKE '%' || ? || '%' OR hosts_creds.password LIKE '%' || ? || '%') ORDER BY {self.sort_field} {self.sort_order}", (self.filter, self.filter, self.filter, self.filter)).fetchall()
        else:
            self.creds = Database.request(f"SELECT hosts.id as host_id, hosts_creds.id, hosts.ip, hosts.hostname, hosts_creds.type, hosts_creds.domain, hosts_creds.username, hosts_creds.password FROM hosts, hosts_creds WHERE hosts.id = hosts_creds.host_id ORDER BY {self.sort_field} {self.sort_order}").fetchall()
        self.layoutChanged.emit()  # https://stackoverflow.com/questions/45359569/how-to-update-qtableview-on-qabstracttablemodel-change

    def rowCount(self, parent):
        return len(self.creds)

    def columnCount(self, parent):
        return len(self.headers)

    def itemData(self, index):
        return self.creds[index.row()]

    def sort(self, col, order):
        self.layoutAboutToBeChanged.emit()
        if col == 2: # Sort by IP address
            # Fuck you sqlite
            self.sort_field = f"""CAST(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')-1) AS INTEGER),
CAST(substr(substr(trim({self.headers[col]}),length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})) ,1, instr(substr(trim({self.headers[col]}),length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})),'.')-1) AS INTEGER),
CAST(substr(substr(trim({self.headers[col]}),length(substr(substr(trim({self.headers[col]}),length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})) ,1, instr(substr(trim({self.headers[col]}),length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})),'.')))+length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})) ,1, instr(substr(trim({self.headers[col]}),length(substr(substr(trim({self.headers[col]}),length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})) ,1, instr(substr(trim({self.headers[col]}),length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})),'.')))+length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})),'.')-1) AS INTEGER),
CAST(substr(trim({self.headers[col]}),length(substr(substr(trim({self.headers[col]}),length(substr(substr(trim({self.headers[col]}),length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})) ,1, instr(substr(trim({self.headers[col]}),length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})),'.')))+length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})) ,1, instr(substr(trim({self.headers[col]}),length(substr(substr(trim({self.headers[col]}),length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})) ,1, instr(substr(trim({self.headers[col]}),length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})),'.')))+length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})),'.')))+ length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+length(substr(substr(trim({self.headers[col]}),length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})) ,1, instr(substr(trim({self.headers[col]}),length(substr(trim({self.headers[col]}),1,instr(trim({self.headers[col]}),'.')))+1,length({self.headers[col]})),'.')))+1,length(trim({self.headers[col]}))) AS INTEGER)"""
        else:
            self.sort_field = self.headers[col]

        if order == Qt.DescendingOrder:
            self.sort_order = "DESC"
        else:
            self.sort_order = "ASC"
        self.update_data()
        self.layoutChanged.emit()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[col]
        return None

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None

        return self.creds[index.row()][self.headers[index.column()].lower()]

    def filter_credstable(self, search_input: str):
        self.filter = search_input
        self.update_data()

    def get_creds_for_host(self, host_id: int) -> list:
        return Database.request('select * from hosts_creds where host_id = ?', (host_id, )).fetchall()

    def create_creds(self, host_id: int) -> int:
        new_id = Database.request("INSERT INTO hosts_creds(host_id) VALUES (?) RETURNING id", (host_id, )).fetchone()['id']
        self.update_data()
        return new_id

    def remove_creds(self, creds_id: int) -> None:
        Database.request("DELETE FROM hosts_creds WHERE id = ?", (creds_id, ))
        self.update_data()

    def update_credentials(self, cred_id: str, column: str, new_value: str):
        Database.request(f"UPDATE hosts_creds SET {column} = ? WHERE id = ?", (new_value, cred_id))
        self.update_data()