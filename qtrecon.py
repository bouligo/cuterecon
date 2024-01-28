import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, Qt

from ui.mainwindow import MainWindow
from core.controller import Controller


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)

    appIcon = QIcon("icons/icon.ico")
    app.setWindowIcon(appIcon)

    window = MainWindow()
    window.show()

    controller = Controller(window)

    # with open("ui/NeonButtons.qss", "r") as f:
    #     _style = f.read()
    #     app.setStyleSheet(_style)

    sys.exit(app.exec())