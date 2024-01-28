from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from datetime import datetime
from core.database import Database

class LogModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.ui = parent
        self.logs = []
        self.headers = ['id', 'Date', 'Type', 'Log'] # Must be the same as column names in db

    def update_data(self):
        self.logs = Database.request("SELECT * FROM logs ORDER BY id ASC").fetchall()

    def rowCount(self, parent):
        return len(self.logs)

    def columnCount(self, parent):
        return len(self.headers)

    def itemData(self, index):
        return self.logs[index.row()]

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None

        return self.logs[index.row()][self.headers[index.column()].lower()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[col]
        return None

    # def sort(self, col, order):
    #     self.layoutAboutToBeChanged.emit()
    #     self.logs = sorted(self.logs, key=operator.itemgetter(col))
    #     if order == Qt.DescendingOrder:
    #         self.logs.reverse()
    #     self.layoutChanged.emit()

    def emit_refresh(self):
        self.layoutChanged.emit()  # https://stackoverflow.com/questions/45359569/how-to-update-qtableview-on-qabstracttablemodel-change
        self.ui.ui.log_table.resizeColumnsToContents()

    def get_log_details(self, index: QModelIndex):
        identifier = index.row() + 1
        if identifier != -1:
            return Database.request('select * from logs where id = ?', (identifier, )).fetchone()
        else:
            return None

    def add_log(self, new_log):
        Database.request('insert into logs values (NULL, ?, ?, ?)', (str(datetime.now().isoformat(' ', 'seconds')), new_log[0], new_log[1]))
        self.update_data()
        self.emit_refresh()