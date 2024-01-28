from PySide6.QtWidgets import QDialog

from ui.ui_set_variables import Ui_Dialog


class Set_Variables(QDialog):
    def __init__(self):
        super(Set_Variables, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
