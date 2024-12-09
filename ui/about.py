from PySide6.QtWidgets import QDialog

from ui.ui_about import Ui_Dialog


class About(QDialog):
    def __init__(self, parent):
        super(About, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
