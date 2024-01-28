from PySide6.QtWidgets import QDialog

from ui.ui_credentials import Ui_creds_dialog


class Credentials_dialog(QDialog):
    def __init__(self):
        super(Credentials_dialog, self).__init__()
        self.ui = Ui_creds_dialog()
        self.ui.setupUi(self)
