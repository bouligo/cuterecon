from PySide6.QtWidgets import QDialog

from ui.ui_custom_command import Ui_Dialog


class Custom_Command(QDialog):
    def __init__(self):
        super(Custom_Command, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
