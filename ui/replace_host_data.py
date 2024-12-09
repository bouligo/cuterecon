from PySide6.QtWidgets import QDialog

from ui.ui_replace_host_data import Ui_replace_host_data


class Replace_host_data(QDialog):
    selected_option = None

    def __init__(self, parent, ip: str, hostname: str):
        super(Replace_host_data, self).__init__(parent)
        self.ui = Ui_replace_host_data()
        self.ui.setupUi(self)

        self.ui.text.setText(f"Host {ip}{' (' + hostname + ')' if hostname else ''} already exist. What do you want to do: ")

        self.ui.merge.clicked.connect(self.merge)
        self.ui.merge_all.clicked.connect(self.merge_all)
        self.ui.erase.clicked.connect(self.erase)
        self.ui.erase_all.clicked.connect(self.erase_all)
        self.ui.keep.clicked.connect(self.keep)
        self.ui.keep_all.clicked.connect(self.keep_all)

    def exec(self):
        super().exec()
        return self.selected_option

    def merge(self):
        self.selected_option = self.ui.merge
        self.accept()

    def merge_all(self):
        self.selected_option = self.ui.merge_all
        self.accept()

    def erase(self):
        self.selected_option = self.ui.erase
        self.accept()

    def erase_all(self):
        self.selected_option = self.ui.erase_all
        self.accept()

    def keep(self):
        self.selected_option = self.ui.keep
        self.reject()

    def keep_all(self):
        self.selected_option = self.ui.keep_all
        self.reject()
