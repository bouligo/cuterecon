from PySide2.QtGui import QCursor, QIcon, QTextCursor
from PySide2.QtWidgets import QApplication, QFileDialog, QTabBar, QTableWidgetItem, QMenu, QTextEdit, QTableWidget, \
    QAbstractItemView, QMessageBox, QInputDialog, QDialog, QLabel, QLineEdit, QHeaderView
from PySide2.QtCore import QPoint, QModelIndex, Qt

import ipaddress  # check input for IP
import netifaces # Get ifaces ip addr

from core.database import Database
from core.config import Config
from ui.custom_command import Custom_Command
from ui.new_scan import New_Scan
from ui.search import Search
from ui.set_variables import Set_Variables
from ui.about import About


class View:
    def __init__(self, main_window, controller):
        self.ui = main_window
        self.controller = controller

        self.default_tabs = [{'name': 'Ports', 'object': type(QTableWidget())},
                             {'name': 'Nmap', 'object': type(QTextEdit())},
                             {'name': 'Notes', 'object': type(QTextEdit())}]
        self.app_tabs = dict()

        self.setup_ui()
        self.connect_slots()

    def setup_ui(self):
        self.ui.ui.actionEnable_automatic_tools.setChecked(Config.get()['user_prefs']['enable_autorun'])
        self.ui.ui.actionAutosave_database_every_5_mins.setChecked(Config.get()['user_prefs']['autosave'])
        self.ui.ui.actionEnable_automatic_tools_on_import.setChecked(Config.get()['user_prefs']['enable_autorun_on_xml_import'])
        self.ui.ui.host_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.reset_ui_snippets()

    def reset_ui_snippets(self):
        for interface_name in Config.get()['user_prefs']['preferred_interfaces']:
            if interface_name in netifaces.interfaces() and netifaces.AF_INET in netifaces.ifaddresses(interface_name).keys():
                self.ui.ui.lhost.setText(netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0]['addr'])
                break
        self.ui.ui.lport.setText(str(Config.get()['user_prefs']['preferred_lport']))
        self.ui.ui.sharename.setText(Config.get()['user_prefs']['preferred_sharename'])
        self.setup_ui_snippets_body()

    def setup_ui_snippets_body(self):
        self.ui.ui.snippets_tabs.clear()
        tabs = {}
        for tab in Config.get()['snippets']:
            tabs[tab] = QTextEdit()
            for title in Config.get()['snippets'][tab]:
                tabs[tab].insertHtml(f"<h3>{title}</h3><br />")
                for content in Config.get()['snippets'][tab][title]:
                    if isinstance(content, list):
                        tabs[tab].insertHtml(f'<h4>{content[0]}</h4><p>')
                        for subcontent in content[1:]:
                            subcontent = subcontent.replace("%%%LHOST%%%", self.ui.ui.lhost.text())
                            subcontent = subcontent.replace("%%%LPORT%%%", self.ui.ui.lport.text())
                            subcontent = subcontent.replace("%%%SHARENAME%%%", self.ui.ui.sharename.text())
                            for char in set(self.ui.ui.escaped_chars.text()):
                                subcontent = subcontent.replace(char, '\\' + char)
                            for char in set(self.ui.ui.urlencoded_chars.text()):
                                subcontent = subcontent.replace(char, '%' + str(ord(char)))
                                subcontent = subcontent.replace(char, '%' + str(ord(char)))
                            tabs[tab].insertPlainText(subcontent)
                            tabs[tab].insertHtml('</p><br />')
                        tabs[tab].insertHtml('<br />')
                    else:
                        content = content.replace("%%%LHOST%%%", self.ui.ui.lhost.text())
                        content = content.replace("%%%LPORT%%%", self.ui.ui.lport.text())
                        content = content.replace("%%%SHARENAME%%%", self.ui.ui.sharename.text())
                        for char in set(self.ui.ui.escaped_chars.text()):
                            content = content.replace(char, '\\' + char)
                        for char in set(self.ui.ui.urlencoded_chars.text()):
                            content = content.replace(char, '%' + str(ord(char)))
                        tabs[tab].insertHtml('<p>')
                        tabs[tab].insertPlainText(content)
                        tabs[tab].insertHtml('</p><br />')

                tabs[tab].insertHtml('<br />')

            tabs[tab].moveCursor(QTextCursor.Start)
            self.ui.ui.snippets_tabs.addTab(tabs[tab], tab)

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
        self.ui.ui.searchbox.textEdited.connect(self.apply_filter_on_host_list)
        self.ui.ui.actionEnable_automatic_tools.triggered.connect(lambda checked: Config.set(["user_prefs", "enable_autorun"], checked))
        self.ui.ui.actionEnable_automatic_tools_on_import.triggered.connect(lambda checked: Config.set(["user_prefs", "enable_autorun_on_xml_import"], checked))
        self.ui.ui.reset_lhost_lport.clicked.connect(self.reset_ui_snippets)
        self.ui.ui.lhost.textEdited.connect(self.setup_ui_snippets_body)
        self.ui.ui.lport.textEdited.connect(self.setup_ui_snippets_body)
        self.ui.ui.escaped_chars.textEdited.connect(self.setup_ui_snippets_body)
        self.ui.ui.urlencoded_chars.textEdited.connect(self.setup_ui_snippets_body)
        self.ui.ui.sharename.textEdited.connect(self.setup_ui_snippets_body)
        self.ui.ui.port_table.itemSelectionChanged.connect(self.change_filter_hosts_for_port)
        self.ui.ui.machine_list_copy_selection_to_clipboard.clicked.connect(self.machine_list_copy_selection_to_clipboard)
        self.ui.ui.machine_list_copy_all_to_clipboard.clicked.connect(self.machine_list_copy_all_to_clipboard)
        self.ui.ui.hosts_for_port_table.customContextMenuRequested.connect(self.right_click_in_hosts_for_port_table)

    def about(self):
        about_dialog = About()
        about_dialog.setWindowTitle("About this program")
        about_dialog.ui.text.setText(f"<h1>QtRecon {self.controller.APPLICATION_VERSION}</h1><p>2023, licenced under Creative Commons <i>CC-BY</i></p><p>Thanks to my friends, for all the advices they gave me and the beta-testing while developping this thing</br ></p><a href='https://github.com/bouligo/cuterecon/'>https://github.com/bouligo/cuterecon/</a>")
        about_dialog.ui.image.setPixmap("icons/icon.ico")
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

    def copy_ip_in_clipboard_from_hostlist(self, index: QModelIndex):
        host = self.controller.get_selected_host(index)
        clipboard = QApplication.clipboard()
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
        # list of colors from doc: https://doc.qt.io/qtforpython-5/PySide2/QtCore/Qt.html#PySide2.QtCore.PySide2.QtCore.Qt.GlobalColor
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
                self.close_right_panel_tabs()
        elif action == set_os_action:
            new_os, confirmed = QInputDialog.getItem(None, "Set Operating System", "Set the OS to :", ["Windows", "Linux", "Unknown"])
            if confirmed:
                self.controller.change_host_os(item, new_os)
                self.close_right_panel_tabs()
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
        filename, _ = QFileDialog.getOpenFileName(caption='Restore saved session', dir='.', filter='*.sqlite')
        if filename:
            self.controller.open_db(filename)

    def save_db(self):
        if not Database.current_savefile:
            self.save_as_db()
        else:
            self.controller.save_db()

    def save_as_db(self):
        filename, _ = QFileDialog.getSaveFileName(caption='Save current session', dir='.', filter='*.sqlite')
        if filename:
            if not filename.endswith('.sqlite'):
                filename += '.sqlite'
            self.controller.save_db(filename)
        
    def dialog_import_xml(self):
        filename, _ = QFileDialog.getOpenFileName(caption='Import nmap XML output', dir='.', filter='*.xml')
        if filename:
            self.controller.log('INFO', f"Importing Nmap results from {filename}")
            new_hosts = self.controller.parse_nmap_xml(filename)

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
                                         new_scan_dialog.ui.os_detection.checkState())

    def update_notes(self):
        current_notes = self.app_tabs['Notes'].toHtml()
        self.controller.update_notes_for_current_host(current_notes)

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
            self.app_tabs[widget['name']] = widget['object']()
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

        # Setup notes signal / slot
        self.app_tabs['Notes'].textChanged.connect(self.update_notes)

        # Delete close button on default tabs
        self.ui.ui.application_TabWidget.tabBar().tabButton(0, QTabBar.RightSide).resize(0, 0)
        self.ui.ui.application_TabWidget.tabBar().tabButton(1, QTabBar.RightSide).resize(0, 0)
        self.ui.ui.application_TabWidget.tabBar().tabButton(2, QTabBar.RightSide).resize(0, 0)

    def update_right_panel(self, host: QModelIndex):
        host_details = self.controller.get_selected_host(host)
        if not host_details:
            return

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

        # Notes
        if 'notes' in host_details.keys():
            self.app_tabs['Notes'].blockSignals(True) # Consumes less resources, and do not trigger the dirty marker on databas
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

    def update_hosts_for_port_panel(self, ports: dict):
        self.ui.ui.port_table.setRowCount(len(ports['udp']) + len(ports['tcp']))

        row_count = 0
        for proto in ['udp', 'tcp']:
            for port in ports[proto]:
                self.ui.ui.port_table.setItem(row_count, 0, QTableWidgetItem(proto))
                self.ui.ui.port_table.setItem(row_count, 1, QTableWidgetItem(str(port)))
                row_count += 1

    def change_filter_hosts_for_port(self):
        port = self.ui.ui.port_table.item(self.ui.ui.port_table.currentRow(),1).text()
        self.controller.filter_hosts_for_port_table(port)

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

    def machine_list_copy_selection_to_clipboard(self):
        data = {}
        for item in self.ui.ui.hosts_for_port_table.selectedIndexes():
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
        clipboard.setText(clipboard_data)
        self.ui.statusBar().showMessage('Data copied to clipboard !', 5000)

    def machine_list_copy_all_to_clipboard(self):
        self.ui.ui.hosts_for_port_table.selectAll()
        self.machine_list_copy_selection_to_clipboard()

