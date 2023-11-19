from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex
from core.database import Database


class CredsModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.ui = parent
        self.creds = []
        self.filter = ""
        self.headers = ['id', 'Hostname', 'Type', 'Domain', 'Username', 'Password'] # Must be the same as column names in db, but exception for host_id

    def update_data(self):
        if self.filter:
            self.creds = Database.request("SELECT hosts_creds.id, hosts.hostname, hosts_creds.type, hosts_creds.domain, hosts_creds.username, hosts_creds.password FROM hosts, hosts_creds WHERE hosts.id == hosts_creds.host_id AND (hosts.hostname LIKE '%' || ? || '%' OR hosts_creds.domain LIKE '%' || ? || '%' OR hosts_creds.username LIKE '%' || ? || '%' OR hosts_creds.password LIKE '%' || ? || '%') ORDER BY hosts_creds.id ASC", (self.filter, self.filter, self.filter, self.filter)).fetchall()
        else:
            self.creds = Database.request("SELECT hosts_creds.id, hosts.hostname, hosts_creds.type, hosts_creds.domain, hosts_creds.username, hosts_creds.password FROM hosts, hosts_creds WHERE hosts.id = hosts_creds.host_id ORDER BY hosts.id ASC").fetchall()
        self.layoutChanged.emit()  # https://stackoverflow.com/questions/45359569/how-to-update-qtableview-on-qabstracttablemodel-change

    def rowCount(self, parent):
        return len(self.creds)

    def columnCount(self, parent):
        return len(self.headers)

    def itemData(self, index):
        return self.creds[index.row()]

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None

        return self.creds[index.row()][self.headers[index.column()].lower()]

    def filter_credstable(self, search_input: str):
        self.filter = search_input
        self.update_data()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[col]
        return None

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