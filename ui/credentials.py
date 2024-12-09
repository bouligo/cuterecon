from PySide6.QtWidgets import QDialog

from ui.ui_credentials import Ui_creds_dialog


class Credentials_dialog(QDialog):
    def __init__(self, parent):
        super(Credentials_dialog, self).__init__(parent)
        self.ui = Ui_creds_dialog()
        self.ui.setupUi(self)
