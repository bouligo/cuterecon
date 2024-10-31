import random
import shlex
import string
import json

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QIcon, QRegularExpressionValidator
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QFrame, QPushButton, QCheckBox, QHBoxLayout, QMessageBox

from core.config import Config
from ui.ui_settings import Ui_Dialog

def order_by_port_number(key):
    try:
        return int(key)
    except ValueError:
        return 0  # ANY is the only string, and should be placed first

class Settings(QDialog):
    config = None
    user_binaries_scrollbar_maxrange = user_variables_scrollbar_maxrange = 0
    user_binaries = {}
    user_variables = {}
    user_binaries_tab_visited_at_least_once = user_variables_tab_visited_at_least_once = False  # To handle automatic scroll for user binaries

    def __init__(self):
        super(Settings, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.config = Config.get()

        self.fill_fields_from_configuration()

        self.ui.tabs.currentChanged.connect(self.tab_changed)

    def accept(self):
        # Check values in tabs
        if self.check_mandatory_fields(True):
            return

        # Paths
        self.config["paths"]['nmap_output_dir'] = self.ui.nmap_output_dir.text()

        # Core binaries
        binary, *args = shlex.split(self.ui.core_binaries_nmap_cmd.text())
        self.config["core_binaries"]['nmap'] = {'binary': binary, 'args': args}
        binary, *args = shlex.split(self.ui.core_binaries_terminal_cmd.text())
        self.config["core_binaries"]['terminal'] = {'binary': binary, 'args': args}
        binary, *args = shlex.split(self.ui.core_binaries_graphicalsu_cmd.text())
        self.config["core_binaries"]['graphical_su'] = {'binary': binary, 'args': args}

        # user_binaries
        self.config["user_binaries"] = self.user_binaries

        # user_prefs
        self.config["user_prefs"]['enable_autorun'] = self.ui.enable_autorun.isChecked()
        self.config["user_prefs"]['enable_autorun_on_xml_import'] = self.ui.enable_autorun_on_xml_import.isChecked()
        self.config["user_prefs"]['confirm_before_tab_removal'] = self.ui.confirm_before_tab_removal.isChecked()
        self.config["user_prefs"]['dev_null_as_stdin'] = self.ui.dev_null_as_stdin.isChecked()
        self.config["user_prefs"]['remove_nmap_xml_files_after_scan'] = self.ui.remove_nmap_xml_files_after_scan.isChecked()
        self.config["user_prefs"]['delete_logs_on_save'] = self.ui.delete_logs_on_save.isChecked()
        self.config["user_prefs"]['autosave'] = self.ui.autosave.isChecked()
        self.config["user_prefs"]['autosave_interval'] = self.ui.autosave_interval.value() * 1000
        self.config["user_prefs"]['preferred_interfaces'] = self.ui.preferred_interfaces.toPlainText().split()
        self.config["user_prefs"]['preferred_lport'] = self.ui.preferred_lport.value()
        self.config["user_prefs"]['monospaced_fonts'] = self.ui.monospaced_fonts.text()

        # autorun + ports_associations + User variables + cleaning
        self.config["autorun"]['tcp'] = {}
        self.config["autorun"]['udp'] = {}
        self.config["ports_associations"]['tcp'] = {}
        self.config["ports_associations"]['udp'] = {}
        for key in self.config["user_binaries"]:
            # autorun
            for port in self.config["user_binaries"][key]['autorun_ports']:
                proto, port_number = port.split('/')
                proto = proto.lower()
                port_number = port_number.lower()  # For ANY
                if port_number in self.config["autorun"][proto].keys():
                    self.config["autorun"][proto][port_number].append(key)
                else:
                    self.config["autorun"][proto][port_number] = [key]

            # ports_associations
            for port in self.config["user_binaries"][key]['associated_ports']:
                proto, port_number = port.split('/')
                proto = proto.lower()
                port_number = port_number.lower()  # For ANY
                if port_number in self.config["ports_associations"][proto].keys():
                    self.config["ports_associations"][proto][port_number].append(key)
                else:
                    self.config["ports_associations"][proto][port_number] = [key]

            del self.config["user_binaries"][key]['frame']
            del self.config["user_binaries"][key]['delete_button']
            del self.config["user_binaries"][key]['autorun_ports']
            del self.config["user_binaries"][key]['associated_ports']

        # Ordering ports for better readability
        self.config["autorun"]['tcp'] = dict(sorted(self.config["autorun"]['tcp'].items(), key=lambda t: order_by_port_number(t[0])))
        self.config["autorun"]['udp'] = dict(sorted(self.config["autorun"]['udp'].items(), key=lambda t: order_by_port_number(t[0])))
        self.config["ports_associations"]['tcp'] = dict(sorted(self.config["ports_associations"]['tcp'].items(), key=lambda t: order_by_port_number(t[0])))
        self.config["ports_associations"]['udp'] = dict(sorted(self.config["ports_associations"]['udp'].items(), key=lambda t: order_by_port_number(t[0])))

        # User variables
        self.config['user_variables'] = {}
        for key in self.user_variables:
            self.config['user_variables'][key] = self.user_variables[key]['value']

        # snippets
        try:
            snippets_user_data = json.loads(self.ui.snippets_content.toPlainText())
            self.config["snippets"] = snippets_user_data
        except json.decoder.JSONDecodeError as e:
            QMessageBox.warning(self, "Error while parsing JSON snippets", "There was an error while parsing the snippet section : input is not a valid JSON.\n"+str(e))
            return

        # Setting new configuration in memory
        Config.set(['paths'], self.config["paths"])
        Config.set(['core_binaries'], self.config["core_binaries"])
        Config.set(['user_binaries'], self.config["user_binaries"])
        Config.set(['ports_associations'], self.config["ports_associations"])
        Config.set(['autorun'], self.config["autorun"])
        Config.set(['user_prefs'], self.config["user_prefs"])
        Config.set(['user_variables'], self.config["user_variables"])
        Config.set(['snippets'], self.config["snippets"])

        # Save the configuration to disk
        Config.save_config()

        # Close the window as expected
        super(Settings, self).accept()

    def check_mandatory_fields(self, force_all_checks=False):
        """

        :param force_all_checks: Checks tab 2 and 4, regardless of the current tab
        :return:
        """
        # User binaries
        if force_all_checks or self.ui.tabs.currentIndex() != 2:

            # Clean red backgrounds
            for i in range(self.layout_user_binaries.count()):
                self.layout_user_binaries.itemAt(i).widget().layout().itemAt(3).widget().setStyleSheet("")
                self.layout_user_binaries.itemAt(i).widget().layout().itemAt(5).widget().setStyleSheet("")
                self.layout_user_binaries.itemAt(i).widget().layout().itemAt(7).widget().setStyleSheet("")

            # Checking tab title (3), text menu (5) and binary path (7)
            for j in [3, 5, 7]:
                if not all([self.layout_user_binaries.itemAt(i).widget().layout().itemAt(j).widget().text() for i in range(self.layout_user_binaries.count())]):
                    QMessageBox.warning(None, "Missing user binary information", "A mandatory information about a user binary is empty. Please set tab title, menu text and binary path to all entries.")
                    self.ui.tabs.setCurrentIndex(2)
                    for i in range(self.layout_user_binaries.count()):
                        widget = self.layout_user_binaries.itemAt(i).widget().layout().itemAt(j).widget()
                        if not widget.text():
                            self.ui.tab_user_binaries_scrollArea.ensureWidgetVisible(widget)
                            widget.setStyleSheet("background-color: rgba(255, 0, 0, 50);")
                            widget.setFocus()
                    return 1

            # Setting internal variable
            self.user_binaries = {}
            for i in range(self.layout_user_binaries.count()):
                frame = self.layout_user_binaries.itemAt(i).widget()
                self.user_binaries[frame.layout().itemAt(1).widget().text()] = {
                    'frame': frame,
                    'name': frame.layout().itemAt(3).widget().text(),
                    'text': frame.layout().itemAt(5).widget().text(),
                    'detached': frame.layout().itemAt(15).widget().isChecked(),
                    'in_terminal': frame.layout().itemAt(17).widget().isChecked(),
                    'edit_before_launch': frame.layout().itemAt(19).widget().isChecked(),
                    'binary': frame.layout().itemAt(7).widget().text(),
                    'icon': frame.layout().itemAt(11).widget().text(),
                    'working_directory': frame.layout().itemAt(13).widget().text(),
                    'args': shlex.split(frame.layout().itemAt(9).widget().text()),
                    'associated_ports': list(filter(None, frame.layout().itemAt(21).widget().text().split(";"))),
                    'autorun_ports': list(filter(None, frame.layout().itemAt(23).widget().text().split(";"))),
                    'delete_button': frame.layout().itemAt(24).widget()
                }

        # User variables
        if force_all_checks or self.ui.tabs.currentIndex() != 4:

            # Clean red backgrounds
            for i in range(self.layout_user_variables.count()):
                self.layout_user_variables.itemAt(i).layout().itemAt(0).widget().setStyleSheet("")
                self.layout_user_variables.itemAt(i).layout().itemAt(0).widget().setStyleSheet("")
                self.layout_user_variables.itemAt(i).layout().itemAt(0).widget().setStyleSheet("")

            # Checking variables names
            if not all([self.layout_user_variables.itemAt(i).layout().itemAt(0).widget().text() for i in range(self.layout_user_variables.count())]):
                QMessageBox.warning(None, "Missing variable name", "A variable name is empty. Please give all your variables a name.")
                self.ui.tabs.setCurrentIndex(4)
                for i in range(self.layout_user_variables.count()):
                    widget = self.layout_user_variables.itemAt(i).layout().itemAt(0).widget()
                    if not widget.text():
                        self.ui.tab_user_variables_scrollArea.ensureWidgetVisible(widget)
                        widget.setStyleSheet("background-color: rgba(255, 0, 0, 50);")
                        widget.setFocus()
                return 1

            # Setting internal variable
            self.user_variables = {}
            for i in range(self.layout_user_variables.count()):
                key = self.layout_user_variables.itemAt(i).layout().itemAt(0).widget().text()
                value = self.layout_user_variables.itemAt(i).layout().itemAt(1).widget().text()
                self.user_variables[key] = {'value': value, 'layout': self.layout_user_variables.itemAt(i).layout()}

    def tab_changed(self):
        # TODO: check mandatory fields in tab 2 and 4
        self.check_mandatory_fields()

        if self.ui.tabs.currentIndex() == 2:
            self.user_binaries_tab_visited_at_least_once = True
        if self.ui.tabs.currentIndex() == 4:
            self.user_variables_tab_visited_at_least_once = True

    def user_binaries_scrollbar_range_changed(self, min, max):
        if self.user_binaries_tab_visited_at_least_once and max > self.user_binaries_scrollbar_maxrange:
            self.ui.tab_user_binaries_scrollArea.verticalScrollBar().setValue(max)
        self.user_binaries_scrollbar_maxrange = max

    def user_variables_scrollbar_range_changed(self, min, max):
        if self.user_variables_tab_visited_at_least_once and max > self.user_variables_scrollbar_maxrange:
            self.ui.tab_user_variables_scrollArea.verticalScrollBar().setValue(max)
        self.user_variables_scrollbar_maxrange = max

    def fill_fields_from_configuration(self):

        # Paths
        self.ui.nmap_output_dir.setText(self.config['paths']['nmap_output_dir'])

        # Core binaries
        nmap_cmd = self.config['core_binaries']['nmap']['binary']
        if self.config['core_binaries']['nmap']['args']:
            nmap_cmd += " " + shlex.join(self.config['core_binaries']['nmap']['args'])
        self.ui.core_binaries_nmap_cmd.setText(nmap_cmd)

        terminal_cmd = self.config['core_binaries']['terminal']['binary']
        if self.config['core_binaries']['terminal']['args']:
            terminal_cmd += " " + shlex.join(self.config['core_binaries']['terminal']['args'])
        self.ui.core_binaries_terminal_cmd.setText(terminal_cmd)

        graphical_su_cmd = self.config['core_binaries']['graphical_su']['binary']
        if self.config['core_binaries']['graphical_su']['args']:
            graphical_su_cmd += " " + shlex.join(self.config['core_binaries']['graphical_su']['args'])
        self.ui.core_binaries_graphicalsu_cmd.setText(graphical_su_cmd)

        # User binaries
        self.layout_user_binaries = QVBoxLayout()
        self.ui.tab_user_binaries_scrollArea_content.setLayout(self.layout_user_binaries)

        search_field = QLineEdit()
        search_field.setClearButtonEnabled(True)
        search_field.addAction(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SystemSearch)), QLineEdit.LeadingPosition)
        search_field.setPlaceholderText("Search...")
        search_field.textChanged.connect(self.user_binaries_search_field_changed)
        self.ui.verticalLayout_4.addWidget(search_field)

        user_binary_add_button = QPushButton("Add new program")
        user_binary_add_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd)))
        user_binary_add_button.setStyleSheet(user_binary_add_button.styleSheet() + "; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(128, 255, 128, 255));")
        user_binary_add_button.clicked.connect(self.user_binaries_add_button_clicked)
        self.ui.verticalLayout_4.addWidget(user_binary_add_button)

        for user_binary in self.config['user_binaries']:
            frame = self.add_new_user_binary(
                user_binary,
                self.config['user_binaries'][user_binary]['name'],
                self.config['user_binaries'][user_binary]['text'],
                self.config['user_binaries'][user_binary]['detached'],
                self.config['user_binaries'][user_binary]['in_terminal'] if 'in_terminal' in self.config['user_binaries'][user_binary].keys() else False,
                self.config['user_binaries'][user_binary]['edit_before_launch'] if 'edit_before_launch' in self.config['user_binaries'][user_binary].keys() else False,
                self.config['user_binaries'][user_binary]['binary'],
                self.config['user_binaries'][user_binary]['icon'] if 'icon' in self.config['user_binaries'][user_binary] else "",
                self.config['user_binaries'][user_binary]['working_directory'] if 'working_directory' in self.config['user_binaries'][user_binary] else "",
                self.config['user_binaries'][user_binary]['args']
            )
            self.layout_user_binaries.addWidget(frame)

        # User preferences

        self.ui.enable_autorun.setChecked(self.config['user_prefs']['enable_autorun'])
        self.ui.enable_autorun_on_xml_import.setChecked(self.config['user_prefs']['enable_autorun_on_xml_import'])
        self.ui.confirm_before_tab_removal.setChecked(self.config['user_prefs']['confirm_before_tab_removal'])
        self.ui.dev_null_as_stdin.setChecked(self.config['user_prefs']['dev_null_as_stdin'])
        self.ui.remove_nmap_xml_files_after_scan.setChecked(self.config['user_prefs']['remove_nmap_xml_files_after_scan'])
        self.ui.delete_logs_on_save.setChecked(self.config['user_prefs']['delete_logs_on_save'])
        self.ui.autosave.setChecked(self.config['user_prefs']['autosave'])
        self.ui.autosave_interval.setValue(self.config['user_prefs']['autosave_interval']/1000)
        self.ui.monospaced_fonts.setText(self.config['user_prefs']['monospaced_fonts'])
        self.ui.preferred_interfaces.setText('\n'.join(self.config['user_prefs']['preferred_interfaces'])),
        self.ui.preferred_lport.setValue(self.config['user_prefs']['preferred_lport'])

        # Custom variables
        self.layout_user_variables = QVBoxLayout()
        self.ui.tab_user_variables_scrollArea_content.setLayout(self.layout_user_variables)

        for i, variable in enumerate(self.config['user_variables']):
            self.add_new_user_variable(variable, self.config['user_variables'][variable])

        custom_variable_add_button = QPushButton("Add new variable")
        custom_variable_add_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd)))
        custom_variable_add_button.setStyleSheet(custom_variable_add_button.styleSheet() + "; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(128, 255, 128, 255));")
        custom_variable_add_button.clicked.connect(self.user_variables_add_button_clicked)
        self.ui.tab_user_variables_layout.addWidget(custom_variable_add_button)

        # Snippets
        snippets = json.dumps(self.config['snippets'], indent=4)
        self.ui.snippets_content.setText(snippets)

        # Connecting signals / slots
        self.ui.tab_user_binaries_scrollArea.verticalScrollBar().rangeChanged.connect(self.user_binaries_scrollbar_range_changed)
        self.ui.tab_user_variables_scrollArea.verticalScrollBar().rangeChanged.connect(self.user_variables_scrollbar_range_changed)

    def user_binaries_add_button_clicked(self):
        new_frame = self.add_new_user_binary()
        self.layout_user_binaries.addWidget(new_frame)

    def user_variables_add_button_clicked(self):
        name_input_widget = self.add_new_user_variable()
        name_input_widget.setFocus()
        name_input_widget.selectAll()

    def add_new_user_variable(self, name: str = "", value: str = "") -> QLineEdit:
        if not name:
            if f'USER_VARIABLE' not in self.user_variables.keys():
                name = f'USER_VARIABLE'
            else:
                i = 1
                while not name:
                    if f'USER_VARIABLE_{i}' not in self.user_variables.keys():
                        name = f'USER_VARIABLE_{i}'
                    i += 1

        layout = QHBoxLayout()
        delete_button = QPushButton()
        delete_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete)))
        delete_button.clicked.connect(lambda: self.delete_user_variable(layout))
        ret = QLineEdit(name)
        layout.addWidget(ret)
        layout.addWidget(QLineEdit(value))
        layout.addWidget(delete_button)
        self.layout_user_variables.addLayout(layout)

        self.user_variables[name] = {'value': value, 'layout': layout}

        return ret

    def add_new_user_binary(self, program_id: str = "", name: str = "", text: str = "", detached: bool = False, in_terminal: bool = False, edit_before_launch: bool = False, binary: str = "", icon: str = "", working_directory: str = "", args: list = list()) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Plain)
        frame.setLineWidth(3)

        if program_id:
            associated_ports = [f'TCP/{i[0].upper()}' for i in self.config['ports_associations']['tcp'].items() if program_id in i[1]]
            associated_ports += [f'UDP/{i[0].upper()}' for i in self.config['ports_associations']['udp'].items() if program_id in i[1]]
            autorun_ports = [f'TCP/{i[0].upper()}' for i in self.config['autorun']['tcp'].items() if program_id in i[1]]
            autorun_ports += [f'UDP/{i[0].upper()}' for i in self.config['autorun']['udp'].items() if program_id in i[1]]
        else:
            program_id = ''.join(random.choices(string.ascii_lowercase, k=20))
            while program_id in self.user_binaries.keys():
                program_id = ''.join(random.choices(string.ascii_lowercase, k=20))

            associated_ports = list()
            autorun_ports = list()

        delete_button = QPushButton("Remove program")
        delete_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove)))
        delete_button.clicked.connect(lambda: self.delete_user_binary(frame))

        self.user_binaries[program_id] = {
            'frame': frame,
            'name': name,
            'text': text,
            'detached': detached,
            'in_terminal': in_terminal,
            'edit_before_launch': edit_before_launch,
            'binary': binary,
            'icon': icon,
            'working_directory': working_directory,
            'args': args,
            'associated_ports': associated_ports,
            'autorun_ports': autorun_ports,
            'delete_button': delete_button
        }

        current_binary_layout = QFormLayout(frame)

        binary_id = QLineEdit()
        binary_id.setValidator(QRegularExpressionValidator(QRegularExpression(r"[A-Za-z_-]+")))
        binary_id.setText(program_id)
        binary_name = QLineEdit()
        binary_name.setText(name)
        binary_text = QLineEdit()
        binary_text.setText(text)
        binary_is_detached = QCheckBox()
        binary_run_in_terminal = QCheckBox()
        binary_is_detached.setChecked(detached)
        binary_run_in_terminal.setChecked(in_terminal)
        binary_is_detached.toggled.connect(lambda x: binary_run_in_terminal.setChecked(False) if not x else x)
        binary_run_in_terminal.toggled.connect(lambda x: binary_is_detached.setChecked(True) if x else x)
        binary_edit_before_launch = QCheckBox()
        binary_edit_before_launch.setChecked(edit_before_launch)
        binary_path = QLineEdit()
        binary_path.setText(binary)
        binary_icon = QLineEdit()
        binary_icon.setPlaceholderText('Optionnal')
        binary_icon.setText(icon)
        binary_working_directory = QLineEdit()
        binary_working_directory.setPlaceholderText('Optionnal')
        binary_working_directory.setText(working_directory)
        binary_args = QLineEdit()
        binary_args.setPlaceholderText('Optionnal')
        binary_args.setText(shlex.join(args))
        binary_associated_ports = QLineEdit()
        binary_associated_ports.setValidator(QRegularExpressionValidator(QRegularExpression(r"((TCP|UDP)/(ANY|[0-9]+);)*")))
        binary_associated_ports.setPlaceholderText('TCP/80;TCP/443;UDP/ANY')
        binary_associated_ports.setText(';'.join(associated_ports))
        binary_autorun_ports = QLineEdit()
        binary_autorun_ports.setValidator(QRegularExpressionValidator(QRegularExpression(r"((TCP|UDP)/(ANY|[0-9]+);)*")))
        binary_autorun_ports.setPlaceholderText('TCP/80;TCP/443;UDP/ANY')
        binary_autorun_ports.setText(';'.join(autorun_ports))

        current_binary_layout.addRow("Unique identifier:", binary_id)
        current_binary_layout.setRowVisible(0, False)
        current_binary_layout.addRow("Tab title:", binary_name)
        current_binary_layout.addRow("Menu text:", binary_text)
        current_binary_layout.addRow("Binary path:", binary_path)
        current_binary_layout.addRow("Binary arguments:", binary_args)
        current_binary_layout.addRow("Binary icon:", binary_icon)
        current_binary_layout.addRow("Working directory:", binary_working_directory)
        current_binary_layout.addRow("Run as separate process:", binary_is_detached)
        current_binary_layout.addRow("Run in terminal:", binary_run_in_terminal)
        current_binary_layout.addRow("Edit cmdline before execution:", binary_edit_before_launch)
        current_binary_layout.addRow("Associated to ports:", binary_associated_ports)
        current_binary_layout.addRow("Autorun for ports:", binary_autorun_ports)

        current_binary_layout.addWidget(self.user_binaries[program_id]['delete_button'])

        return frame

    def delete_user_binary(self, frame: QFrame):
        for key, value in self.user_binaries.items():
            if value['frame'] == frame:
                frame.deleteLater()
                del self.user_binaries[key]
                break

    def delete_user_variable(self, layout: QHBoxLayout):
        while layout.count():
            item = layout.takeAt(0)
            item.widget().deleteLater()
            layout.removeItem(item)

        for key, value in self.user_variables.items():
            if self.user_variables[key]["layout"] == layout:
                del self.user_variables[key]
                break

        for i in range(self.layout_user_variables.count()):
            _ = self.layout_user_variables.itemAt(i)
            if _ == layout:
                self.layout_user_variables.removeItem(_)
                del layout
                break

    def user_binaries_search_field_changed(self, search_input: str):
        for i in range(self.layout_user_binaries.count()):
            frame = self.layout_user_binaries.itemAt(i).widget()
            frame.setVisible(any([search_input in form_input for form_input in [frame.layout().itemAt(3).widget().text(), frame.layout().itemAt(5).widget().text(), frame.layout().itemAt(7).widget().text()]]))