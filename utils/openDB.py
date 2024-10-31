from PySide6.QtCore import QThread, Signal, QObject, QSize, Qt
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QLabel, QHBoxLayout, QMessageBox, QFrame

from core.database import Database


class Thread_hostmodel(QObject):
    finished = Signal()

    def __init__(self, caller, filename):
        super().__init__()
        self.caller = caller
        self.filename = filename

    def open_db(self):
        exception = Database.import_DB(self.filename)

        if exception:
            QMessageBox.critical(None, 'Could not load session', 'Exception occurred: ' + str(exception))
        else:
            self.caller.host_model.update_data()
            self.caller.hosts_for_port_model.update_data()
            self.caller.update_hosts_for_port_panel()
            self.caller.log_model.update_data()
            self.caller.creds_model.update_data()
            self.caller.log('RUNTIME', f"Restored session {self.filename}")
            Database.has_unsaved_data = False
            self.caller.ui.ui.actionAutosave_database_every_5_mins.setEnabled(True)

        self.caller.ui.ui.host_list.clearSelection()
        self.caller.log_model.layoutChanged.emit()

        self.finished.emit()


class Popup_open_db(QFrame):
    def __init__(self, caller, filename: str):
        super().__init__()
        self.icon = QLabel()
        movie = QMovie("icons/loading.gif")
        movie.setScaledSize(QSize(40, 40))
        self.icon.setMovie(movie)
        movie.start()

        self.label = QLabel("Opening database...")
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setWindowTitle('')
        self.setFixedHeight(70)
        self.setFixedWidth(200)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setObjectName("popup_open_db")
        self.setStyleSheet("QFrame#popup_open_db {background-color:#dfdfdf; border: 1px solid black}")
        self.setLineWidth(10)

        self.worker = Thread_hostmodel(caller, filename)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.thread.quit)
        self.thread.started.connect(self.worker.open_db)
        self.thread.finished.connect(self.close)
        self.thread.start()
