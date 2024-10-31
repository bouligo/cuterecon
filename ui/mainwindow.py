from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QMessageBox, QLineEdit

from core.database import Database
from ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.host_list_filter.addAction(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SystemSearch)), QLineEdit.LeadingPosition)

    def closeEvent(self, event):
        if Database.has_unsaved_data:
            reply = QMessageBox.question(self, "Confirmation needed",
                                           "There are currently unsaved data. Are you sure you want to exit the program?", QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
