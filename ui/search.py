from PySide2.QtWidgets import QDialog

from ui.ui_search import Ui_Dialog


class Search(QDialog):
    def __init__(self):
        super(Search, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
