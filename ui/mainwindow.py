from PySide6.QtWidgets import QMainWindow, QMessageBox

from core.database import Database
from ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def closeEvent(self, event):
        if Database.has_unsaved_data:
            reply = QMessageBox.question(self, "Confirmation needed",
                                           "There are currently unsaved data. Are you sure you want to exit the program?", QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()