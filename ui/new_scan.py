from PySide6.QtWidgets import QDialog

from ui.ui_new_scan import Ui_Dialog


class New_Scan(QDialog):
    def __init__(self):
        super(New_Scan, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
