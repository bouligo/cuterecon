import re

from PySide6.QtGui import QCursor, QIcon, QTextCursor
from PySide6.QtWidgets import QApplication, QFileDialog, QTabBar, QTableWidgetItem, QMenu, QTextEdit, QTableWidget, \
    QAbstractItemView, QMessageBox, QInputDialog, QDialog, QLabel, QLineEdit, QHeaderView, QWidget, QComboBox, \
    QTableView
from PySide6.QtCore import QPoint, QModelIndex, Qt

import ipaddress  # check input for IP
import netifaces # Get ifaces ip addr
import html # To escape text from snippets

from core.database import Database
from core.config import Config
from ui.custom_command import Custom_Command
from ui.new_scan import New_Scan
from ui.search import Search
from ui.set_variables import Set_Variables
from ui.about import About
from ui.credentials import Credentials_dialog
from utils.QNoteTextEdit import QNoteTextEdit


class View:
    def __init__(self, main_window, controller):
        self.ui = main_window
        self.controller = controller

        self.default_tabs = [{'name': 'Ports', 'object': type(QTableWidget())},
                             {'name': 'Nmap', 'object': type(QTextEdit())},
                             {'name': 'Credentials', 'object': type(QTableWidget())},
                             {'name': 'Notes', 'object': type(QNoteTextEdit())}]
        self.app_tabs = dict()

        self.setup_ui()
        self.connect_slots()

    def setup_ui(self):
        self.ui.ui.host_list.setColumnHidden(0, True)
        self.ui.ui.hosts_for_port_table.setColumnHidden(0, True)
        self.ui.ui.creds_table.setColumnHidden(0, True)
        self.ui.ui.creds_table.setColumnHidden(1, True)
        self.ui.ui.log_table.setColumnHidden(0, True)
        self.ui.ui.job_table.setColumnHidden(0, True)
        self.ui.ui.job_table.setColumnHidden(1, True)
        self.ui.ui.job_table.setColumnHidden(2, True)
        self.ui.ui.job_table.setColumnHidden(6, True)
        self.ui.ui.hosts_for_port_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.ui.creds_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.ui.actionEnable_automatic_tools.setChecked(Config.get()['user_prefs']['enable_autorun'])
        self.ui.ui.actionAutosave_database_every_5_mins.setChecked(Config.get()['user_prefs']['autosave'])
        self.ui.ui.actionEnable_automatic_tools_on_import.setChecked(Config.get()['user_prefs']['enable_autorun_on_xml_import'])
        self.ui.ui.host_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        if 'screenshots' in Config.get().keys():
            if 'engine' in Config.get()['screenshots'].keys() and Config.get()['screenshots']['engine'] == "external":
                self.ui.ui.radioButton_screenshots_external.toggle()
            if 'interval' in Config.get()['screenshots'].keys():
                self.ui.ui.spinBox_screenshots_interval.setValue(Config.get()['screenshots']['interval'])
                self.ui.ui.progressBar.setMaximum(Config.get()['screenshots']['interval'])
            if 'dst_folder' in Config.get()['screenshots'].keys(): self.ui.ui.screenshot_dst_folder.setText(Config.get()['screenshots']['dst_folder'])
            if 'work_folder' in Config.get()['screenshots'].keys(): self.ui.ui.screenshot_work_folder.setText(Config.get()['screenshots']['work_folder'])
            if 'pixel_threshold_different_images' in Config.get()['screenshots'].keys(): self.ui.ui.pixel_slider.setValue(Config.get()['screenshots']['pixel_threshold_different_images'])
            if 'check_locked_screen_cmd' in Config.get()['screenshots'].keys(): self.ui.ui.cmd_check_lockscreen.setText(Config.get()['screenshots']['check_locked_screen_cmd'])
            if 'check_locked_screen_cmd_result' in Config.get()['screenshots'].keys(): self.ui.ui.cmd_check_result_lockscreen.setText(Config.get()['screenshots']['check_locked_screen_cmd_result'])
            if 'screenshot_cmd' in Config.get()['screenshots'].keys(): self.ui.ui.screenshot_cmd.setText(Config.get()['screenshots']['screenshot_cmd'])
            if 'check_locked_screen' in Config.get()['screenshots'].keys():
                if Config.get()['screenshots']['check_locked_screen']:
                    self.ui.ui.checkBox_screenshot_lockscreen.setCheckState(Qt.CheckState.Checked)
                else:
                    self.ui.ui.cmd_check_lockscreen.setEnabled(False)
                    self.ui.ui.cmd_check_result_lockscreen.setEnabled(False)
            if 'ignore_if_active_window' in Config.get()['screenshots'].keys() and Config.get()['screenshots']['ignore_if_active_window']: self.ui.ui.checkBox_screenshot_ignore_if_active_window.setCheckState(Qt.CheckState.Checked)
            if 'convert_png_to_jpg' in Config.get()['screenshots'].keys() and Config.get()['screenshots']['convert_png_to_jpg']: self.ui.ui.checkBox_screenshot_jpg.setCheckState(Qt.CheckState.Checked)
            if 'include_processes' in Config.get()['screenshots'].keys() and Config.get()['screenshots']['include_processes']: self.ui.ui.checkBox_screenshot_processes.setCheckState(Qt.CheckState.Checked)
            if 'include_ocr' in Config.get()['screenshots'].keys() and Config.get()['screenshots']['include_ocr']: self.ui.ui.checkBox_screenshot_ocr.setCheckState(Qt.CheckState.Checked)

        self.reset_ui_snippets()

    def reset_ui_snippets(self):
        for interface_name in Config.get()['user_prefs']['preferred_interfaces']:
            if interface_name in netifaces.interfaces() and netifaces.AF_INET in netifaces.ifaddresses(interface_name).keys():
                self.ui.ui.lhost.setText(netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0]['addr'])
                break
        self.ui.ui.lport.setText(str(Config.get()['user_prefs']['preferred_lport']))
        self.setup_ui_snippets_body()

    def setup_ui_snippets_body(self):
        # Good luck.
        def create_subsection(level: int, content):
            final_subsection = ""
            for i, chunk in enumerate(content):
                current_string = ""
                if isinstance(chunk, str):
                    for char in set(self.ui.ui.escaped_chars.text()):
                        chunk = chunk.replace(char, '\\' + char)
                    for char in set(self.ui.ui.urlencoded_chars.text()):
                        chunk = chunk.replace(char, '%' + str(ord(char)))
                    chunk = html.escape(chunk)
                    if i != len(content)-1 and isinstance(content[i+1], list):
                        current_string += f'<h{level + 4}>{chunk}</h{level + 4}>'
                    else:
                        current_string += chunk + '<br />'
                elif isinstance(chunk, list):
                    if final_subsection and '<h' not in final_subsection:
                        final_subsection = f'<p style="background-color: black; color: white; font-family: Hack, DejaVu Sans Mono, Droid Sans Mono, Courier;">{final_subsection}</p>'
                    current_string += create_subsection(level+1, chunk)

                if '<h' in current_string:
                    if (i == len(content)-1 or isinstance(content[i+1], list)) and final_subsection and '<h' not in final_subsection and '<p' not in final_subsection:
                        final_subsection = f'<p style="background-color: black; color: white; font-family: Hack, DejaVu Sans Mono, Droid Sans Mono, Courier;">{final_subsection}</p>'
                    final_subsection += current_string
                else:
                    final_subsection += current_string
                    if (i == len(content)-1 or isinstance(content[i+1], list)) and final_subsection and '<h' not in final_subsection and '<p' not in final_subsection:
                        final_subsection = f'<p style="background-color: black; color: white; font-family: Hack, DejaVu Sans Mono, Droid Sans Mono, Courier;">{final_subsection}</p>'

            if final_subsection and '<h' not in final_subsection:
                final_subsection = f'<p style="background-color: black; color: white; font-family: Hack, DejaVu Sans Mono, Droid Sans Mono, Courier;">{final_subsection}</p>'

            # Clean-up
            final_subsection = re.sub('(<p[^>]+>)(<p[^>]+>)+', '\\1', final_subsection)
            final_subsection = re.sub('(</p>)(</p>)+', '\\1', final_subsection)
            final_subsection = re.sub('<br /></p>', '</p>', final_subsection)

            return final_subsection

        self.ui.ui.snippets_tabs.clear()
        tabs = {}
        for i, tab in enumerate(Config.get()['snippets']):
            tabs[i] = QTextEdit()
            if not isinstance(Config.get()['snippets'][tab], list):
                continue
            section = ""
            for element in Config.get()['snippets'][tab]:
                if isinstance(element, str):
                    section += f'<h3>{element}</h3>'
                if isinstance(element, list):
                    section += create_subsection(0, element)

            section = section.replace("%%%LHOST%%%", self.ui.ui.lhost.text())
            section = section.replace("%%%LPORT%%%", self.ui.ui.lport.text())

            tabs[i].setHtml(section)
            tabs[i].moveCursor(QTextCursor.Start)
            self.ui.ui.snippets_tabs.addTab(tabs[i], tab)

    def connect_slots(self):
        self.ui.ui.actionNew.triggered.connect(self.controller.clear_db)
        self.ui.ui.actionOpen.triggered.connect(self.open_db)
        self.ui.ui.actionSave.triggered.connect(self.save_db)
        self.ui.ui.actionSaveAs.triggered.connect(self.save_as_db)
        self.ui.ui.actionExit.triggered.connect(self.ui.close)
        self.ui.ui.actionSet_variables.triggered.connect(self.set_variables)
        self.ui.ui.actionSearch_string.triggered.connect(self.dialog_search)
        self.ui.ui.actionReload_configuration_from_file.triggered.connect(self.controller.reload_conf)
        self.ui.ui.actionAbout.triggered.connect(self.about)
        self.ui.ui.actionAbout_Qt.triggered.connect(QApplication.aboutQt)
        self.ui.ui.ImportNmap.clicked.connect(self.dialog_import_xml)
        self.ui.ui.ScanHost.clicked.connect(self.dialog_scan_host)
        self.ui.ui.host_list.clicked.connect(self.update_right_panel)
        self.ui.ui.button_play.clicked.connect(self.clicked_button_play)
        self.ui.ui.button_pause.clicked.connect(self.clicked_button_pause)
        self.ui.ui.button_stop.clicked.connect(self.clicked_button_stop)
        self.ui.ui.job_table.clicked.connect(self.enable_buttons)
        self.ui.ui.host_list.doubleClicked.connect(self.copy_ip_in_clipboard_from_hostlist)
        self.ui.ui.host_list.customContextMenuRequested.connect(self.right_click_in_host_table)
        self.ui.ui.job_table.customContextMenuRequested.connect(self.right_click_in_job_table)
        self.ui.ui.log_table.customContextMenuRequested.connect(self.right_click_in_log_table)
        self.ui.ui.application_TabWidget.tabCloseRequested.connect(self.remove_tab)
        self.ui.ui.host_list_filter.textEdited.connect(self.apply_filter_on_host_list)
        self.ui.ui.creds_table_filter.textEdited.connect(self.apply_filter_on_creds_table)
        self.ui.ui.creds_table.customContextMenuRequested.connect(self.right_click_in_creds_table)
        self.ui.ui.creds_table_copy_selection_to_clipboard.clicked.connect(lambda: self.copy_selectedIndexes_to_clipboard(self.ui.ui.creds_table.selectedIndexes()))
        self.ui.ui.creds_table_copy_all_to_clipboard.clicked.connect(self.creds_table_copy_all_to_clipboard)
        self.ui.ui.creds_table_view_in_host_tab.clicked.connect(lambda: self.switch_to_host_tab(self.ui.ui.creds_table))
        self.ui.ui.actionEnable_automatic_tools.triggered.connect(lambda checked: Config.set(["user_prefs", "enable_autorun"], checked))
        self.ui.ui.actionEnable_automatic_tools_on_import.triggered.connect(lambda checked: Config.set(["user_prefs", "enable_autorun_on_xml_import"], checked))
        self.ui.ui.reset_lhost_lport.clicked.connect(self.reset_ui_snippets)
        self.ui.ui.lhost.textEdited.connect(self.setup_ui_snippets_body)
        self.ui.ui.lport.textEdited.connect(self.setup_ui_snippets_body)
        self.ui.ui.escaped_chars.textEdited.connect(self.setup_ui_snippets_body)
        self.ui.ui.urlencoded_chars.textEdited.connect(self.setup_ui_snippets_body)
        self.ui.ui.port_table.itemSelectionChanged.connect(self.change_filter_hosts_for_port)
        self.ui.ui.machine_list_view_in_host_tab.clicked.connect(lambda: self.switch_to_host_tab(self.ui.ui.hosts_for_port_table))
        self.ui.ui.machine_list_copy_selection_to_clipboard.clicked.connect(lambda: self.copy_selectedIndexes_to_clipboard(self.ui.ui.hosts_for_port_table.selectedIndexes()))
        self.ui.ui.machine_list_copy_all_to_clipboard.clicked.connect(self.machine_list_copy_all_to_clipboard)
        self.ui.ui.hosts_for_port_table.customContextMenuRequested.connect(self.right_click_in_hosts_for_port_table)
        self.ui.ui.button_start_screenshot.clicked.connect(self.button_start_screenshot_clicked)
        self.ui.ui.button_save_screenshot.clicked.connect(self.button_save_screenshots_clicked)

    def about(self):
        about_dialog = About()
        about_dialog.setWindowTitle("About this program")
        about_dialog.ui.text.setText(f"<h1>QtRecon {self.controller.APPLICATION_VERSION}</h1><p>2023, licenced under Creative Commons <i>CC-BY</i></p><p>Thanks to my friends, for all the advices they gave me and the beta-testing while developping this thing</br ></p><a href='https://github.com/bouligo/cuterecon/'>https://github.com/bouligo/cuterecon/</a>")
        # about_dialog.ui.image.setPixmap("icons/icon.ico")  # Integrated in UI now
        about_dialog.ui.button.clicked.connect(about_dialog.close)
        about_dialog.exec()

    def dialog_search(self):
        search_dialog = Search()
        search_dialog.ui.search_button.clicked.connect(lambda: self.search(search_dialog))
        search_dialog.ui.host_list.currentRowChanged.connect(lambda: self.search_in_host(search_dialog))
        search_dialog.exec()

    def search(self, search_dialog: QDialog):
        search_dialog.ui.host_list.clear()
        search_dialog.ui.results.clear()
        search_dialog.ui.host_list.addItems(self.controller.search_string_in_db_hosts(search_dialog.ui.search_input.text()))

    def search_in_host(self, search_dialog: QDialog):
        if search_dialog.ui.host_list.currentItem() is None:
            return
        search_dialog.ui.results.setText('\n'.join(
            self.controller.search_string_in_db_hosts(search_dialog.ui.search_input.text(),
            search_dialog.ui.host_list.currentItem().text())))

    def set_variables(self):
        set_variables_dialog = Set_Variables()
        config_variables = Config.get()['user_variables']
        dialog_variables = {} #Storing Widgets to get inputs easily
        for i, variable in enumerate(config_variables):
            input_field = QLineEdit(config_variables[variable])
            dialog_variables[variable] = input_field
            set_variables_dialog.ui.formLayout.insertRow(i, QLabel(variable + ':'), input_field)

        if not set_variables_dialog.exec():
            return

        for variable in dialog_variables:
            Config.set(["user_variables", variable], dialog_variables[variable].text())

    def button_start_screenshot_clicked(self):
        self.controller.start_or_pause_screenshotting(
            self.ui.ui.radioButton_screenshots_qt.isChecked(),
            self.ui.ui.spinBox_screenshots_interval.value(),
            self.ui.ui.screenshot_dst_folder.text(),
            self.ui.ui.screenshot_work_folder.text(),
            self.ui.ui.pixel_slider.value(),
            self.ui.ui.cmd_check_lockscreen.text(),
            self.ui.ui.cmd_check_result_lockscreen.text(),
            self.ui.ui.screenshot_cmd.text(),
            self.ui.ui.checkBox_screenshot_lockscreen.isChecked(),
            self.ui.ui.checkBox_screenshot_ignore_if_active_window.isChecked(),
            self.ui.ui.checkBox_screenshot_jpg.isChecked(),
            self.ui.ui.checkBox_screenshot_processes.isChecked(),
            self.ui.ui.checkBox_screenshot_ocr.isChecked())

    def button_save_screenshots_clicked(self):
        self.controller.stop_screenshotting()

    def select_credentials_dialog(self, credentials: list) -> (str, str, str, str):
        select_credentials_dialog = Credentials_dialog()
        for i, credential in enumerate(credentials):
            select_credentials_dialog.ui.creds_table.insertRow(select_credentials_dialog.ui.creds_table.rowCount())
            select_credentials_dialog.ui.creds_table.setItem(i, 0, QTableWidgetItem(credential['type']))
            select_credentials_dialog.ui.creds_table.setItem(i, 1, QTableWidgetItem(credential['domain']))
            select_credentials_dialog.ui.creds_table.setItem(i, 2, QTableWidgetItem(credential['username']))
            select_credentials_dialog.ui.creds_table.setItem(i, 3, QTableWidgetItem(credential['password']))
        select_credentials_dialog.ui.creds_table.selectRow(0)
        select_credentials_dialog.exec()

        if select_credentials_dialog.result():
            # Returns type, domain, username and password
            return [cell.data() for cell in select_credentials_dialog.ui.creds_table.selectedIndexes()]
        else:
            return None, None, None, None

    def enable_buttons(self, index: QModelIndex):
        job_details = self.controller.get_job_details(index)
        if job_details['state'] == 'Running':
            self.ui.ui.button_play.setEnabled(False)
            self.ui.ui.button_pause.setEnabled(True)
            self.ui.ui.button_stop.setEnabled(True)
        elif job_details['state'] == 'NotRunning':
            self.ui.ui.button_play.setEnabled(True)
            self.ui.ui.button_pause.setEnabled(False)
            self.ui.ui.button_stop.setEnabled(True)
        else:
            self.ui.ui.button_play.setEnabled(False)
            self.ui.ui.button_pause.setEnabled(False)
            self.ui.ui.button_stop.setEnabled(False)

    def refresh_buttons(self):
        if self.ui.ui.job_table.selectedIndexes():
            self.enable_buttons(self.ui.ui.job_table.selectedIndexes()[0])

    def clicked_button_play(self):
        selected_row = self.ui.ui.job_table.selectedIndexes()
        job_details = self.controller.get_job_details(selected_row[0])  # Choosing first cell to get the job details
        self.controller.resume_job(job_details['id'])
        self.ui.ui.button_play.setEnabled(False)
        self.ui.ui.button_pause.setEnabled(True)

    def clicked_button_pause(self):
        selected_row = self.ui.ui.job_table.selectedIndexes()
        job_details = self.controller.get_job_details(selected_row[0])  # Choosing first cell to get the job details
        self.controller.pause_job(job_details['id'])
        self.ui.ui.button_play.setEnabled(True)
        self.ui.ui.button_pause.setEnabled(False)

    def clicked_button_stop(self):
        selected_row = self.ui.ui.job_table.selectedIndexes()
        job_details = self.controller.get_job_details(selected_row[0]) # Choosing first cell to get the job details
        self.controller.kill_job(job_details['id'])
        self.ui.ui.button_play.setEnabled(False)
        self.ui.ui.button_pause.setEnabled(False)
        self.ui.ui.button_stop.setEnabled(False)

    def apply_filter_on_host_list(self, search_input: str):
        self.controller.filter_hostlist(search_input)

    def apply_filter_on_creds_table(self, search_input: str):
        self.controller.filter_credstable(search_input)

    def copy_ip_in_clipboard_from_hostlist(self, index: QModelIndex):
        host = self.controller.get_selected_host(index)
        clipboard = QApplication.clipboard()
        if index.column() == 3:
            clipboard.setText(host['hostname'])
            self.ui.statusBar().showMessage('Hostname copied to clipboard !', 5000)
        else:
            clipboard.setText(host['ip'])
            self.ui.statusBar().showMessage('IP copied to clipboard !', 5000)


    def right_click_in_host_table(self, qpoint: QPoint):
        item = self.ui.ui.host_list.indexAt(qpoint)
        if item.row() == -1:
            return

        self.update_right_panel(item)
        host = self.controller.get_selected_host(item)

        top_menu = QMenu(None)
        set_ip_action = top_menu.addAction("Change IP")
        set_hostname_action = top_menu.addAction("Set / Change hostname")
        set_os_action = top_menu.addAction("Set / Change OS")
        set_pwned = top_menu.addAction("(Un-)Mark as pwned")
        set_color = top_menu.addMenu("Highlight with color ...")
        color_menu_dict = {}

        color_menu_dict['None'] = set_color.addAction('None')
        set_color.addSeparator()
        # list of colors from doc: https://doc.qt.io/qtforpython-5/PySide6/QtCore/Qt.html#PySide6.QtCore.PySide6.QtCore.Qt.GlobalColor
        for color in ["white", "red", "green", "cyan", "magenta", "yellow", "darkRed", "darkGreen", "blue", "darkBlue", "darkCyan", "darkMagenta", "darkYellow", "gray", "darkGray", "lightGray", "black"]:
            color_menu_dict[color] = set_color.addAction(color)

        top_menu.addSeparator()
        autorun_action = top_menu.addAction("Run all autorun configured programs")
        top_menu.addSeparator()
        remove_action = top_menu.addAction("Delete host and data")

        action = top_menu.exec_(QCursor.pos())
        if not action:
            return

        if action == remove_action:
            self.controller.delete_host(item)
            self.ui.ui.host_list.clearSelection()
            self.close_right_panel_tabs()
        elif action == set_ip_action:
            new_ip, confirmed = QInputDialog.getText(None, "Change IP", "Set the IP address to :", text = host['ip'])
            if confirmed:
                try:
                    ipaddress.IPv4Address(new_ip) # fails if not a valid IP address
                    if host['ip'] != new_ip:
                        self.controller.change_host_ip(item, new_ip)
                        self.close_right_panel_tabs()
                except ipaddress.AddressValueError:
                    QMessageBox.critical(None, "Cannot change IP", f"Cannot change ip address of \"{host['ip']}\" to \"{new_ip}\"")
        elif action == set_hostname_action:
            new_hostname, confirmed = QInputDialog.getText(None, "Set hostname", "Set the hostname to :", text = host['hostname'])
            if confirmed:
                self.controller.change_host_hostname(item, new_hostname)
                # self.close_right_panel_tabs()
        elif action == set_os_action:
            new_os, confirmed = QInputDialog.getItem(None, "Set Operating System", "Set the OS to :", ["Windows", "Linux", "IOS", "Unknown"], editable=False)
            if confirmed:
                self.controller.change_host_os(item, new_os)
                # self.close_right_panel_tabs()
        elif action == set_pwned:
            self.controller.set_host_pwned(item)
        elif action in color_menu_dict.values():
            if action.text() == 'None': # 'd better not trust this ? Use the key from color_menu_dict instead ?
                self.controller.set_host_highlight_color(item, "")
            else:
                self.controller.set_host_highlight_color(item, action.text())
        elif action == autorun_action:
            self.controller.autorun([host['id']])

    def right_click_in_log_table(self, qpoint: QPoint):
        item = self.ui.ui.log_table.indexAt(qpoint)
        log = self.ui.ui.log_table.model().itemData(item)

        if not log:
            return

        top_menu = QMenu(None)
        clipboard_action = top_menu.addAction("Copy log into clipboard")
        clipboard_action.setIcon(QIcon.fromTheme("edit-copy"))

        action = top_menu.exec_(QCursor.pos())
        if not action:
            return

        if action == clipboard_action:
            clipboard = QApplication.clipboard()
            clipboard.setText(log['log'])

    def right_click_in_job_table(self, qpoint: QPoint):
        item = self.ui.ui.job_table.indexAt(qpoint)
        job = self.controller.get_job_details(item)

        if not job:
            return

        command = job['command']

        top_menu = QMenu(None)
        clipboard_action = top_menu.addAction("Copy command into clipboard")
        clipboard_action.setIcon(QIcon.fromTheme("edit-copy"))

        action = top_menu.exec_(QCursor.pos())
        if not action:
            return

        if action == clipboard_action:
            clipboard = QApplication.clipboard()
            clipboard.setText(command)

    def right_click_in_port_table(self, qpoint: QPoint):
        item = self.app_tabs['Ports'].itemAt(qpoint)
        if item is None:
            return

        host = self.ui.ui.host_list.model().itemData(self.ui.ui.host_list.currentIndex())
        port = self.app_tabs['Ports'].item(item.row(), 2).text()
        proto = self.app_tabs['Ports'].item(item.row(), 0).text()
        description = self.app_tabs['Ports'].item(item.row(), 3).text()

        top_menu, visible_actions = self.create_actions_from_port(proto, port)

        custom_command = top_menu.addAction("Custom command ...")
        copy_description = top_menu.addAction("Copy service description into clipboard")
        copy_description.setIcon(QIcon.fromTheme("edit-copy"))
        copy_uri = top_menu.addAction(f"Copy \"{host['ip']}:{port}\" into clipboard")
        copy_uri.setIcon(QIcon.fromTheme("edit-copy"))
        action = top_menu.exec_(QCursor.pos())

        if not action:
            return

        if action == copy_description:
            clipboard = QApplication.clipboard()
            clipboard.setText(description)

        if action == copy_uri:
            clipboard = QApplication.clipboard()
            clipboard.setText(f"{host['ip']}:{port}")

        if action == custom_command:
            self.launch_custom_command_dialog()

        for program in visible_actions:
            if program['text'] == action.text():
                self.controller.new_job(program)
                return

    def right_click_in_hosts_for_port_table(self, qpoint: QPoint):
        item = self.ui.ui.hosts_for_port_table.indexAt(qpoint) # But we're not using this here, as multiple selection can occur
        if item is None:
            return

        proto = self.ui.ui.port_table.item(self.ui.ui.port_table.currentRow(),0).text()
        port = self.ui.ui.port_table.item(self.ui.ui.port_table.currentRow(),1).text()
        hosts = dict()
        for index in self.ui.ui.hosts_for_port_table.selectedIndexes():
            itemData = self.ui.ui.hosts_for_port_table.model().itemData(index)
            if itemData['id'] not in hosts.keys():
                hosts[itemData['id']] = itemData

        top_menu, visible_actions = self.create_actions_from_port(proto, port)
        custom_command = top_menu.addAction("Custom command ...")
        action = top_menu.exec_(QCursor.pos())

        if not action:
            return

        if action == custom_command:
            self.launch_custom_command_dialog()

        for program in visible_actions:
            if program['text'] == action.text():
                for host in hosts:
                    self.controller.new_job(program, hosts[host]['id'], port)
                return

    def right_click_in_creds_table(self, qpoint: QPoint):
        if self.ui.ui.work.currentIndex() == 0: # Calling from a host
            widget_calling = self.app_tabs['Credentials']
        elif self.ui.ui.work.currentIndex() == 2:  # Calling from the credentials tab
            widget_calling = self.ui.ui.creds_table

        item = widget_calling.indexAt(qpoint)

        if item is None:
            return

        top_menu = QMenu()

        if item.row() >= 0 or item.column() >= 0:
            clipboard_action = top_menu.addAction("Copy selected cells into clipboard")
            clipboard_action.setIcon(QIcon.fromTheme("edit-copy"))
            delete_action = top_menu.addAction("Delete credentials")
            delete_action.setIcon(QIcon.fromTheme("edit-delete"))
            if self.ui.ui.work.currentIndex() == 0:
                top_menu.addSeparator()
        if self.ui.ui.work.currentIndex() == 0:
            insert_action = top_menu.addAction("Insert new credentials")
            insert_action.setIcon(QIcon.fromTheme("document-new"))

        action = top_menu.exec_(QCursor.pos())
        if not action:
            return

        if self.ui.ui.work.currentIndex() == 0 and action == insert_action:
            widget_calling.insertRow(widget_calling.rowCount())
            new_id = self.controller.create_creds()
            widget_calling.setItem(widget_calling.rowCount()-1, 0, QTableWidgetItem(str(new_id)))

            combo = QComboBox()
            combo.addItems(["password", "hash", "ssh_key", "other"])
            combo.setProperty('cred_id', str(new_id))
            widget_calling.setCellWidget(widget_calling.rowCount()-1, 1, combo)
            combo.currentTextChanged.connect(lambda new_type, qcombobox=combo: self.credentials_changed(qcombobox)) # signal in loop: https://stackoverflow.com/questions/46300229/connecting-multiples-signal-slot-in-a-for-loop-in-pyqt

        elif action == clipboard_action:
            self.copy_selectedIndexes_to_clipboard(widget_calling.selectedIndexes())

        elif action == delete_action:
            items = widget_calling.selectedIndexes()

            creds_ids = []
            rows_to_delete = []
            for item in items:
                if self.ui.ui.work.currentIndex() == 0:
                    creds_ids.append(widget_calling.item(item.row(), 0).text())
                    rows_to_delete.append(item.row())
                if self.ui.ui.work.currentIndex() == 2:
                    creds_ids.append(item.model().itemData(item)['id'])

            self.controller.remove_creds(list(set(creds_ids)))

            if self.ui.ui.work.currentIndex() == 0:
                for row in reversed(sorted(rows_to_delete)):
                    self.app_tabs['Credentials'].removeRow(int(row))
            if self.ui.ui.work.currentIndex() == 2:
                self.reset_right_panel()

    def launch_custom_command_dialog(self):
        new_scan_dialog = Custom_Command()
        new_scan_dialog.ui.detached.stateChanged.connect(lambda checked: new_scan_dialog.in_terminal.setEnabled(checked))

        if new_scan_dialog.exec():
            command = new_scan_dialog.ui.command.text()

            if command:
                program = {
                    'name': command.split()[0],
                    'binary': command.split()[0],
                    'args': command.split()[1:],
                    'detached': new_scan_dialog.ui.detached.checkState() == Qt.CheckState.Checked,
                    'in_terminal': new_scan_dialog.ui.in_terminal.checkState() == Qt.CheckState.Checked
                }
                self.controller.new_job(program)

    def create_actions_from_port(self, proto: str, port: str):
        port_associations = Config.get()['ports_associations']
        user_binaries = Config.get()['user_binaries']
        visible_actions = []  # Storing proposed actions here, rather than parsing AGAIN the conf ...

        top_menu = QMenu(None)

        for current_port in ["any", port]:
            if current_port != "any" and port not in port_associations[proto].keys():
                top_menu.addAction(f"No specific program declared for port {current_port}/{proto}").setEnabled(False)
            else:
                if current_port == "any" and "any" not in Config.get()['ports_associations'][proto]:
                    continue
                for program in port_associations[proto][current_port]:
                    _ = top_menu.addAction(user_binaries[program]['text'])
                    if 'icon' in user_binaries[program].keys():
                        _.setIcon(QIcon(user_binaries[program]['icon']))
                    elif 'in_terminal' in user_binaries[program].keys() and user_binaries[program]['in_terminal']:
                        _.setIcon(QIcon.fromTheme("utilities-terminal"))

                    visible_actions.append(user_binaries[program])

            top_menu.addSeparator()

        return top_menu, visible_actions


    def open_db(self):
        filename, _ = QFileDialog.getOpenFileName(caption='Restore saved session', filter='*.sqlite')
        if filename:
            self.controller.open_db(filename)

    def save_db(self):
        if not Database.current_savefile:
            self.save_as_db()
        else:
            self.controller.save_db()

    def save_as_db(self):
        filename, _ = QFileDialog.getSaveFileName(caption='Save current session', filter='*.sqlite')
        if filename:
            if not filename.endswith('.sqlite'):
                filename += '.sqlite'
            self.controller.save_db(filename)

    def dialog_import_xml(self):
        filename, _ = QFileDialog.getOpenFileName(caption='Import nmap XML output', filter='*.xml')
        if filename:
            self.controller.log('INFO', f"Importing Nmap results from {filename}")
            new_hosts = self.controller.parse_nmap_data('xml', filename)

            if Config.get()['user_prefs']['enable_autorun_on_xml_import']:
                self.controller.autorun(new_hosts)

    def dialog_scan_host(self):
        new_scan_dialog = New_Scan()
        if new_scan_dialog.exec():
            target = new_scan_dialog.ui.target.text()
            nmap_speed = new_scan_dialog.ui.nmap_speed.text()
            ports = new_scan_dialog.ui.ports.text()
            if target:
                self.controller.new_scan(target, nmap_speed, ports,
                                         new_scan_dialog.ui.skip_host_discovery.checkState(),
                                         new_scan_dialog.ui.check_versions.checkState(),
                                         new_scan_dialog.ui.launch_scripts.checkState(),
                                         new_scan_dialog.ui.os_detection.checkState(),
                                         new_scan_dialog.ui.tcp_and_udp.checkState())

    def update_notes(self):
        current_notes = self.app_tabs['Notes'].toHtml()
        self.controller.update_notes_for_current_host(current_notes)

    def credentials_changed(self, item: QComboBox | QTableWidgetItem):
        columns_description = {0: "id", 1: "type", 2: "domain", 3: "username", 4: "password"}
        if type(item) == QComboBox: # Type of cred has changed
            self.controller.update_credentials(item.property('cred_id'), columns_description[1], item.currentText())
        elif type(item) == QTableWidgetItem: # Any cell other than the credential type has changed
            cred_id = self.app_tabs['Credentials'].item(item.row(), 0).text()
            self.controller.update_credentials(cred_id, columns_description[item.column()], item.text())

    def new_tab(self, title: str, job_id: int, content: str = "") -> QTextEdit:
        tab = QTextEdit(content)
        tab.setReadOnly(True)
        tab_index = self.ui.ui.application_TabWidget.addTab(tab, title)
        self.app_tabs[tab_index] = {'widget': tab, 'job_id': job_id}
        self.link_job_and_widget(job_id, tab)
        return tab

    def link_job_and_widget(self, job_id: int, widget: QTextEdit):
        if self.controller.get_job(job_id):
            job = self.controller.get_job(job_id)
            job.readyReadStandardOutput.connect(lambda: widget.setText(job.get_output_text().replace(chr(0), "")))
            job.readyReadStandardError.connect(lambda: widget.setText(job.get_output_text().replace(chr(0), "")))

    def close_right_panel_tabs(self):
        for i in range(self.ui.ui.application_TabWidget.count()):
            self.ui.ui.application_TabWidget.removeTab(0)
        self.app_tabs = {}

    def reset_right_panel(self):
        self.close_right_panel_tabs()

        for widget in self.default_tabs:
            if issubclass(widget['object'], QWidget):
                self.app_tabs[widget['name']] = widget['object']()
            else:
                self.app_tabs[widget['name']] = QWidget()
            self.ui.ui.application_TabWidget.addTab(self.app_tabs[widget['name']], widget['name'])

        # Setup ports view
        self.app_tabs['Ports'].setColumnCount(4)
        self.app_tabs['Ports'].setHorizontalHeaderLabels(['Protocol', 'Status','Port','Description'])
        self.app_tabs['Ports'].verticalHeader().setVisible(False)
        self.app_tabs['Ports'].horizontalHeader().setStretchLastSection(True)
        self.app_tabs['Ports'].setGridStyle(Qt.DotLine)
        self.app_tabs['Ports'].setSelectionBehavior(QAbstractItemView.SelectRows)
        self.app_tabs['Ports'].setSelectionMode(QAbstractItemView.SingleSelection)
        self.app_tabs['Ports'].setContextMenuPolicy(Qt.CustomContextMenu)
        self.app_tabs['Ports'].setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Setup nmap tab
        self.app_tabs['Nmap'].setReadOnly(True)

        # Setup creds tab
        self.app_tabs['Credentials'].setColumnCount(5)
        self.app_tabs['Credentials'].setColumnHidden(0, True)
        self.app_tabs['Credentials'].setHorizontalHeaderItem(0, QTableWidgetItem('id'))
        self.app_tabs['Credentials'].setHorizontalHeaderItem(1, QTableWidgetItem('type'))
        self.app_tabs['Credentials'].setHorizontalHeaderItem(2, QTableWidgetItem('domain'))
        self.app_tabs['Credentials'].setHorizontalHeaderItem(3, QTableWidgetItem('username'))
        self.app_tabs['Credentials'].setHorizontalHeaderItem(4, QTableWidgetItem('password'))
        self.app_tabs['Credentials'].horizontalHeader().setStretchLastSection(True)
        self.app_tabs['Credentials'].itemChanged.connect(self.credentials_changed)
        self.app_tabs['Credentials'].setContextMenuPolicy(Qt.CustomContextMenu)
        self.app_tabs['Credentials'].customContextMenuRequested.connect(self.right_click_in_creds_table)

        # Setup notes signal / slot
        self.app_tabs['Notes'].textChanged.connect(self.update_notes)

        # Delete close button on default tabs
        self.ui.ui.application_TabWidget.tabBar().tabButton(0, QTabBar.RightSide).resize(0, 0)
        self.ui.ui.application_TabWidget.tabBar().tabButton(1, QTabBar.RightSide).resize(0, 0)
        self.ui.ui.application_TabWidget.tabBar().tabButton(2, QTabBar.RightSide).resize(0, 0)
        self.ui.ui.application_TabWidget.tabBar().tabButton(3, QTabBar.RightSide).resize(0, 0)

    def update_right_panel(self, host: QModelIndex):
        host_details = self.controller.get_selected_host(host)
        if not host_details:
            return

        current_index = self.ui.ui.application_TabWidget.currentIndex()

        self.reset_right_panel()

        ## Filling default tabs
        # Port listing
        self.app_tabs['Ports'].setRowCount(len(host_details['ports'])) # Number of row to add (counting number of ports in both tcp and udp)

        row_count = 0
        for port in host_details['ports']:
            self.app_tabs['Ports'].setItem(row_count, 0, QTableWidgetItem(port['proto']))
            self.app_tabs['Ports'].setItem(row_count, 1, QTableWidgetItem(port['status']))
            self.app_tabs['Ports'].setItem(row_count, 2, QTableWidgetItem(port['port']))
            self.app_tabs['Ports'].setItem(row_count, 3, QTableWidgetItem(port['description']))

            row_count += 1

        # Connect the right click on a row
        self.app_tabs['Ports'].customContextMenuRequested.connect(self.right_click_in_port_table)

        # Nmap output
        if 'nmap' in host_details.keys():
            self.app_tabs['Nmap'].setText(host_details['nmap'])

        # Credentials
        self.app_tabs['Credentials'].blockSignals(True)
        self.app_tabs['Credentials'].setRowCount(len(host_details['credentials']))
        for row in range(len(host_details['credentials'])):
            combo = QComboBox()
            combo.addItems(["password", "hash", "ssh_key", "other"])
            self.app_tabs['Credentials'].setCellWidget(row, 1, combo)

        for i, cred in enumerate(host_details['credentials']):
            self.app_tabs['Credentials'].setItem(i, 0, QTableWidgetItem(str(cred['id'])))
            self.app_tabs['Credentials'].cellWidget(i, 1).setCurrentText(str(cred['type']))
            self.app_tabs['Credentials'].cellWidget(i, 1).setProperty('cred_id', str(cred['id']))
            self.app_tabs['Credentials'].cellWidget(i, 1).currentTextChanged.connect(lambda new_type, qcombobox=self.app_tabs['Credentials'].cellWidget(i, 1): self.credentials_changed(qcombobox)) # signal in loop: https://stackoverflow.com/questions/46300229/connecting-multiples-signal-slot-in-a-for-loop-in-pyqt
            self.app_tabs['Credentials'].setItem(i, 2, QTableWidgetItem(str(cred['domain'])))
            self.app_tabs['Credentials'].setItem(i, 3, QTableWidgetItem(str(cred['username'])))
            self.app_tabs['Credentials'].setItem(i, 4, QTableWidgetItem(str(cred['password'])))

        self.app_tabs['Credentials'].blockSignals(False)

        # Notes
        if 'notes' in host_details.keys():
            self.app_tabs['Notes'].blockSignals(True) # Consumes less resources, and do not trigger the dirty marker on database
            try:
                self.app_tabs['Notes'].setHtml(host_details['notes'])
            except ValueError:
                self.app_tabs['Notes'].setHtml(host_details['notes'].replace(chr(0), ""))
            self.app_tabs['Notes'].blockSignals(False)

        ## Application tabs
        for app in host_details['external_tabs']:
            if app['text']:
                self.new_tab(app['title'], app['job_id'], app['text'].replace(chr(0), ""))
            else:
                self.new_tab(app['title'], app['job_id'], "")

        # Restoring tab focus if currentIndex < 4
        if current_index < 4:
            self.ui.ui.application_TabWidget.setCurrentIndex(current_index)


    def update_hosts_for_port_panel(self, ports: dict):
        self.ui.ui.port_table.setRowCount(len(ports['udp']) + len(ports['tcp']))

        row_count = 0
        for proto in ['udp', 'tcp']:
            for port in ports[proto]:
                self.ui.ui.port_table.setItem(row_count, 0, QTableWidgetItem(proto))
                self.ui.ui.port_table.setItem(row_count, 1, QTableWidgetItem(str(port)))
                row_count += 1

    def change_filter_hosts_for_port(self):
        proto = port = ""
        if self.ui.ui.port_table.item(self.ui.ui.port_table.currentRow(),0):
            proto = self.ui.ui.port_table.item(self.ui.ui.port_table.currentRow(),0).text()
        if self.ui.ui.port_table.item(self.ui.ui.port_table.currentRow(),1):
            port = self.ui.ui.port_table.item(self.ui.ui.port_table.currentRow(),1).text()
        if proto and port:
            self.controller.filter_hosts_for_port_table(proto, port)

    def remove_tab(self, tab_index: int):
        # There is a job, It is running, User wants to confirm
        if Config.get()['user_prefs']['confirm_before_tab_removal']:
            question = "Tab content will be discarded. Are you sure ?"
            if self.controller.get_job(self.app_tabs[tab_index]['job_id']):
                job = self.controller.get_job(self.app_tabs[tab_index]['job_id'])
                if job.state() == 2:
                    question = "The currently running program will be killed, and tab content will be discarded. Are you sure ?"

            if QMessageBox.question(None, 'Confirmation', question) != QMessageBox.Yes:
                return

        self.controller.remove_tab(self.app_tabs[tab_index])

        # Removing and re-indexing internal view app_tabs
        del self.app_tabs[tab_index]
        if range(tab_index, len(self.app_tabs)):
            for i in range(tab_index, len(self.app_tabs)):
                self.app_tabs[i] = self.app_tabs[i+1]
            del self.app_tabs[i+1]

        self.ui.ui.application_TabWidget.removeTab(tab_index)

    def copy_selectedIndexes_to_clipboard(self, selectedIndexes: list):
        data = {}
        for item in selectedIndexes:
            if item.data() is None:
                continue
            if item.row() in data.keys():
                data[item.row()].append(item.data())
            else:
                data[item.row()] = [item.data()]

        clipboard_data = ""
        for key in data:
            clipboard_data += ';'.join(data[key]) + '\n'

        clipboard = QApplication.clipboard()
        clipboard.setText(clipboard_data.strip('\n'))
        self.ui.statusBar().showMessage('Data copied to clipboard !', 5000)

    def machine_list_copy_all_to_clipboard(self):
        self.ui.ui.hosts_for_port_table.selectAll()
        self.copy_selectedIndexes_to_clipboard(self.ui.ui.hosts_for_port_table.selectedIndexes())

    def creds_table_copy_all_to_clipboard(self):
        self.ui.ui.creds_table.selectAll()
        self.copy_selectedIndexes_to_clipboard(self.ui.ui.creds_table.selectedIndexes())

    def switch_to_host_tab(self, tableview: QTableView):
        selectedRows = set([i.row() for i in tableview.selectedIndexes()])
        if len(selectedRows) > 1:
            QMessageBox.warning(None, "Error", "Please select only one host at a time.")
            return
        if len(selectedRows) == 0:
            QMessageBox.warning(None, "Error", "Please select a host to view it in the Hosts tab.")
            return

        self.controller.switch_to_host(tableview.model().itemData(tableview.selectedIndexes()[0])['host_id'])