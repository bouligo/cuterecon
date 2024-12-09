from PySide6.QtWidgets import QDialog

from ui.ui_search import Ui_Dialog


class Search(QDialog):
    def __init__(self, parent):
        super(Search, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
