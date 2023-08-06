from PySide2.QtWidgets import QDialog

from ui.ui_about import Ui_Dialog


class About(QDialog):
    def __init__(self):
        super(About, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
