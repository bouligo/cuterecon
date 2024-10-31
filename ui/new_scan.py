from PySide6.QtWidgets import QDialog

from core.config import Config
from ui.ui_new_scan import Ui_Dialog


class New_Scan(QDialog):
    def __init__(self):
        super(New_Scan, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.ports.setText(Config.get()['nmap_options']['ports'])
        for i in range(self.ui.type.count()):  # .findText() doesn't work for some reason...
            if Config.get()['nmap_options']['type'] in self.ui.type.itemText(i):
                self.ui.type.setCurrentIndex(i)
        self.ui.nmap_speed.setValue(int(Config.get()['nmap_options']['speed'][-1]))
        self.ui.additional_args.setText(Config.get()['nmap_options']['additional_args'])
        self.ui.skip_host_discovery.setChecked(Config.get()['nmap_options']['skip_host_discovery'])
        self.ui.check_versions.setChecked(Config.get()['nmap_options']['version_probing'])
        self.ui.launch_scripts.setChecked(Config.get()['nmap_options']['default_scripts'])
        self.ui.os_detection.setChecked(Config.get()['nmap_options']['os_detection'])
        self.ui.tcp_and_udp.setChecked(Config.get()['nmap_options']['tcp_and_udp'])
