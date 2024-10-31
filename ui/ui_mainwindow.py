# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowXdfPzQ.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QFormLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QProgressBar, QPushButton, QRadioButton, QSizePolicy,
    QSlider, QSpacerItem, QSpinBox, QSplitter,
    QStatusBar, QTabWidget, QTableView, QTableWidget,
    QTableWidgetItem, QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 836)
        MainWindow.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionNew.setEnabled(True)
        icon = QIcon(QIcon.fromTheme(u"document-new"))
        self.actionNew.setIcon(icon)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionOpen.setEnabled(True)
        icon1 = QIcon(QIcon.fromTheme(u"document-open"))
        self.actionOpen.setIcon(icon1)
        self.actionSaveAs = QAction(MainWindow)
        self.actionSaveAs.setObjectName(u"actionSaveAs")
        self.actionSaveAs.setEnabled(True)
        icon2 = QIcon(QIcon.fromTheme(u"document-save"))
        self.actionSaveAs.setIcon(icon2)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        icon3 = QIcon(QIcon.fromTheme(u"application-exit"))
        self.actionExit.setIcon(icon3)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionSettings.setEnabled(True)
        icon4 = QIcon(QIcon.fromTheme(u"preferences-system"))
        self.actionSettings.setIcon(icon4)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        icon5 = QIcon(QIcon.fromTheme(u"help-about"))
        self.actionAbout.setIcon(icon5)
        self.actionAbout_Qt = QAction(MainWindow)
        self.actionAbout_Qt.setObjectName(u"actionAbout_Qt")
        self.actionTools = QAction(MainWindow)
        self.actionTools.setObjectName(u"actionTools")
        self.actionTools.setEnabled(False)
        icon6 = QIcon(QIcon.fromTheme(u"applications-utilities"))
        self.actionTools.setIcon(icon6)
        self.actionEnable_automatic_tools = QAction(MainWindow)
        self.actionEnable_automatic_tools.setObjectName(u"actionEnable_automatic_tools")
        self.actionEnable_automatic_tools.setCheckable(True)
        self.actionEnable_automatic_tools.setChecked(True)
        self.actionEnable_automatic_tools_on_import = QAction(MainWindow)
        self.actionEnable_automatic_tools_on_import.setObjectName(u"actionEnable_automatic_tools_on_import")
        self.actionEnable_automatic_tools_on_import.setCheckable(True)
        self.actionEnable_automatic_tools_on_import.setChecked(False)
        self.actionSearch_string = QAction(MainWindow)
        self.actionSearch_string.setObjectName(u"actionSearch_string")
        self.actionSearch_string.setEnabled(True)
        icon7 = QIcon(QIcon.fromTheme(u"edit-find"))
        self.actionSearch_string.setIcon(icon7)
        self.actionSave_running_conf_as_persistent = QAction(MainWindow)
        self.actionSave_running_conf_as_persistent.setObjectName(u"actionSave_running_conf_as_persistent")
        self.actionSave_running_conf_as_persistent.setEnabled(False)
        self.actionReload_configuration_from_file = QAction(MainWindow)
        self.actionReload_configuration_from_file.setObjectName(u"actionReload_configuration_from_file")
        icon8 = QIcon(QIcon.fromTheme(u"view-refresh"))
        self.actionReload_configuration_from_file.setIcon(icon8)
        self.actionAutosave_database_every_5_mins = QAction(MainWindow)
        self.actionAutosave_database_every_5_mins.setObjectName(u"actionAutosave_database_every_5_mins")
        self.actionAutosave_database_every_5_mins.setCheckable(True)
        self.actionAutosave_database_every_5_mins.setEnabled(False)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave.setIcon(icon2)
        self.actionSet_variables = QAction(MainWindow)
        self.actionSet_variables.setObjectName(u"actionSet_variables")
        self.actionDelete_hosts_with_no_services = QAction(MainWindow)
        self.actionDelete_hosts_with_no_services.setObjectName(u"actionDelete_hosts_with_no_services")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.work = QTabWidget(self.splitter)
        self.work.setObjectName(u"work")
        self.work.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.work.sizePolicy().hasHeightForWidth())
        self.work.setSizePolicy(sizePolicy)
        self.hosts = QWidget()
        self.hosts.setObjectName(u"hosts")
        self.horizontalLayout_6 = QHBoxLayout(self.hosts)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.splitter_2 = QSplitter(self.hosts)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.splitter_2.setOpaqueResize(False)
        self.layoutWidget = QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.host_list = QTableView(self.layoutWidget)
        self.host_list.setObjectName(u"host_list")
        self.host_list.setMinimumSize(QSize(330, 0))
        font = QFont()
        font.setPointSize(12)
        self.host_list.setFont(font)
        self.host_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.host_list.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.host_list.setEditTriggers(QAbstractItemView.EditTrigger.AnyKeyPressed|QAbstractItemView.EditTrigger.CurrentChanged|QAbstractItemView.EditTrigger.DoubleClicked|QAbstractItemView.EditTrigger.EditKeyPressed)
        self.host_list.setAlternatingRowColors(True)
        self.host_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.host_list.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.host_list.horizontalHeader().setMinimumSectionSize(30)
        self.host_list.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_5.addWidget(self.host_list)

        self.host_list_filter = QLineEdit(self.layoutWidget)
        self.host_list_filter.setObjectName(u"host_list_filter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.host_list_filter.sizePolicy().hasHeightForWidth())
        self.host_list_filter.setSizePolicy(sizePolicy1)
        self.host_list_filter.setClearButtonEnabled(True)

        self.verticalLayout_5.addWidget(self.host_list_filter)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ImportNmap = QPushButton(self.layoutWidget)
        self.ImportNmap.setObjectName(u"ImportNmap")

        self.horizontalLayout.addWidget(self.ImportNmap)

        self.ScanHost = QPushButton(self.layoutWidget)
        self.ScanHost.setObjectName(u"ScanHost")

        self.horizontalLayout.addWidget(self.ScanHost)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.splitter_2.addWidget(self.layoutWidget)
        self.application_TabWidget = QTabWidget(self.splitter_2)
        self.application_TabWidget.setObjectName(u"application_TabWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.application_TabWidget.sizePolicy().hasHeightForWidth())
        self.application_TabWidget.setSizePolicy(sizePolicy2)
        self.application_TabWidget.setTabsClosable(True)
        self.splitter_2.addWidget(self.application_TabWidget)

        self.horizontalLayout_6.addWidget(self.splitter_2)

        self.work.addTab(self.hosts, "")
        self.services = QWidget()
        self.services.setObjectName(u"services")
        self.services.setEnabled(True)
        self.horizontalLayout_2 = QHBoxLayout(self.services)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.port_table = QTableWidget(self.services)
        if (self.port_table.columnCount() < 2):
            self.port_table.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.port_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.port_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.port_table.setObjectName(u"port_table")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.port_table.sizePolicy().hasHeightForWidth())
        self.port_table.setSizePolicy(sizePolicy3)
        self.port_table.setMinimumSize(QSize(300, 0))
        self.port_table.setFont(font)
        self.port_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.port_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.port_table.horizontalHeader().setStretchLastSection(True)
        self.port_table.verticalHeader().setVisible(False)

        self.horizontalLayout_2.addWidget(self.port_table)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.hosts_for_port_table = QTableView(self.services)
        self.hosts_for_port_table.setObjectName(u"hosts_for_port_table")
        self.hosts_for_port_table.setFont(font)
        self.hosts_for_port_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.hosts_for_port_table.setAlternatingRowColors(True)
        self.hosts_for_port_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.hosts_for_port_table.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_6.addWidget(self.hosts_for_port_table)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.machine_list_view_in_host_tab = QPushButton(self.services)
        self.machine_list_view_in_host_tab.setObjectName(u"machine_list_view_in_host_tab")

        self.horizontalLayout_7.addWidget(self.machine_list_view_in_host_tab)

        self.machine_list_copy_selection_to_clipboard = QPushButton(self.services)
        self.machine_list_copy_selection_to_clipboard.setObjectName(u"machine_list_copy_selection_to_clipboard")
        icon9 = QIcon(QIcon.fromTheme(u"edit-copy"))
        self.machine_list_copy_selection_to_clipboard.setIcon(icon9)

        self.horizontalLayout_7.addWidget(self.machine_list_copy_selection_to_clipboard)

        self.machine_list_copy_all_to_clipboard = QPushButton(self.services)
        self.machine_list_copy_all_to_clipboard.setObjectName(u"machine_list_copy_all_to_clipboard")
        self.machine_list_copy_all_to_clipboard.setIcon(icon9)

        self.horizontalLayout_7.addWidget(self.machine_list_copy_all_to_clipboard)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        self.work.addTab(self.services, "")
        self.creds = QWidget()
        self.creds.setObjectName(u"creds")
        self.verticalLayout_7 = QVBoxLayout(self.creds)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.creds_table = QTableView(self.creds)
        self.creds_table.setObjectName(u"creds_table")
        self.creds_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.creds_table.setSortingEnabled(True)
        self.creds_table.horizontalHeader().setMinimumSectionSize(100)
        self.creds_table.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_7.addWidget(self.creds_table)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.creds_table_filter = QLineEdit(self.creds)
        self.creds_table_filter.setObjectName(u"creds_table_filter")
        self.creds_table_filter.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_8.addWidget(self.creds_table_filter)

        self.creds_table_view_in_host_tab = QPushButton(self.creds)
        self.creds_table_view_in_host_tab.setObjectName(u"creds_table_view_in_host_tab")

        self.horizontalLayout_8.addWidget(self.creds_table_view_in_host_tab)

        self.creds_table_copy_selection_to_clipboard = QPushButton(self.creds)
        self.creds_table_copy_selection_to_clipboard.setObjectName(u"creds_table_copy_selection_to_clipboard")
        self.creds_table_copy_selection_to_clipboard.setIcon(icon9)

        self.horizontalLayout_8.addWidget(self.creds_table_copy_selection_to_clipboard)

        self.creds_table_copy_all_to_clipboard = QPushButton(self.creds)
        self.creds_table_copy_all_to_clipboard.setObjectName(u"creds_table_copy_all_to_clipboard")
        self.creds_table_copy_all_to_clipboard.setIcon(icon9)

        self.horizontalLayout_8.addWidget(self.creds_table_copy_all_to_clipboard)


        self.verticalLayout_7.addLayout(self.horizontalLayout_8)

        self.work.addTab(self.creds, "")
        self.snippets = QWidget()
        self.snippets.setObjectName(u"snippets")
        self.snippets.setEnabled(True)
        self.verticalLayout_4 = QVBoxLayout(self.snippets)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.snippets)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.lhost = QLineEdit(self.snippets)
        self.lhost.setObjectName(u"lhost")

        self.horizontalLayout_4.addWidget(self.lhost)

        self.label = QLabel(self.snippets)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.lport = QLineEdit(self.snippets)
        self.lport.setObjectName(u"lport")

        self.horizontalLayout_4.addWidget(self.lport)

        self.label_4 = QLabel(self.snippets)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.escaped_chars = QLineEdit(self.snippets)
        self.escaped_chars.setObjectName(u"escaped_chars")

        self.horizontalLayout_4.addWidget(self.escaped_chars)

        self.label_5 = QLabel(self.snippets)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.urlencoded_chars = QLineEdit(self.snippets)
        self.urlencoded_chars.setObjectName(u"urlencoded_chars")

        self.horizontalLayout_4.addWidget(self.urlencoded_chars)

        self.reset_lhost_lport = QPushButton(self.snippets)
        self.reset_lhost_lport.setObjectName(u"reset_lhost_lport")

        self.horizontalLayout_4.addWidget(self.reset_lhost_lport)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.snippets_tabs = QTabWidget(self.snippets)
        self.snippets_tabs.setObjectName(u"snippets_tabs")

        self.horizontalLayout_5.addWidget(self.snippets_tabs)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.work.addTab(self.snippets, "")
        self.screenshots = QWidget()
        self.screenshots.setObjectName(u"screenshots")
        self.verticalLayout_8 = QVBoxLayout(self.screenshots)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_10 = QLabel(self.screenshots)
        self.label_10.setObjectName(u"label_10")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_10)

        self.label_7 = QLabel(self.screenshots)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.screenshot_cmd = QLineEdit(self.screenshots)
        self.screenshot_cmd.setObjectName(u"screenshot_cmd")
        self.screenshot_cmd.setEnabled(False)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.screenshot_cmd)

        self.label_6 = QLabel(self.screenshots)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_6)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.screenshot_work_folder = QLineEdit(self.screenshots)
        self.screenshot_work_folder.setObjectName(u"screenshot_work_folder")

        self.horizontalLayout_11.addWidget(self.screenshot_work_folder)

        self.toolButton_2 = QToolButton(self.screenshots)
        self.toolButton_2.setObjectName(u"toolButton_2")

        self.horizontalLayout_11.addWidget(self.toolButton_2)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_11)

        self.label_3 = QLabel(self.screenshots)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.screenshot_dst_folder = QLineEdit(self.screenshots)
        self.screenshot_dst_folder.setObjectName(u"screenshot_dst_folder")

        self.horizontalLayout_12.addWidget(self.screenshot_dst_folder)

        self.toolButton = QToolButton(self.screenshots)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout_12.addWidget(self.toolButton)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_12)

        self.label_9 = QLabel(self.screenshots)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(200, 16777215))

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_9)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.spinBox_screenshots_interval = QSpinBox(self.screenshots)
        self.spinBox_screenshots_interval.setObjectName(u"spinBox_screenshots_interval")
        self.spinBox_screenshots_interval.setMaximumSize(QSize(100, 16777215))
        self.spinBox_screenshots_interval.setValue(15)

        self.horizontalLayout_14.addWidget(self.spinBox_screenshots_interval)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_14)

        self.label_8 = QLabel(self.screenshots)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_8)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.pixel_slider = QSlider(self.screenshots)
        self.pixel_slider.setObjectName(u"pixel_slider")
        self.pixel_slider.setMaximum(5000)
        self.pixel_slider.setSingleStep(10)
        self.pixel_slider.setPageStep(100)
        self.pixel_slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_10.addWidget(self.pixel_slider)

        self.label_slider = QLabel(self.screenshots)
        self.label_slider.setObjectName(u"label_slider")

        self.horizontalLayout_10.addWidget(self.label_slider)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_10)

        self.checkBox_screenshot_lockscreen = QCheckBox(self.screenshots)
        self.checkBox_screenshot_lockscreen.setObjectName(u"checkBox_screenshot_lockscreen")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.checkBox_screenshot_lockscreen)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.cmd_check_lockscreen = QLineEdit(self.screenshots)
        self.cmd_check_lockscreen.setObjectName(u"cmd_check_lockscreen")

        self.horizontalLayout_13.addWidget(self.cmd_check_lockscreen)

        self.cmd_check_result_lockscreen = QLineEdit(self.screenshots)
        self.cmd_check_result_lockscreen.setObjectName(u"cmd_check_result_lockscreen")
        sizePolicy1.setHeightForWidth(self.cmd_check_result_lockscreen.sizePolicy().hasHeightForWidth())
        self.cmd_check_result_lockscreen.setSizePolicy(sizePolicy1)
        self.cmd_check_result_lockscreen.setMinimumSize(QSize(170, 0))

        self.horizontalLayout_13.addWidget(self.cmd_check_result_lockscreen)


        self.formLayout.setLayout(6, QFormLayout.FieldRole, self.horizontalLayout_13)

        self.checkBox_screenshot_ignore_if_active_window = QCheckBox(self.screenshots)
        self.checkBox_screenshot_ignore_if_active_window.setObjectName(u"checkBox_screenshot_ignore_if_active_window")
        self.checkBox_screenshot_ignore_if_active_window.setChecked(False)

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.checkBox_screenshot_ignore_if_active_window)

        self.checkBox_screenshot_jpg = QCheckBox(self.screenshots)
        self.checkBox_screenshot_jpg.setObjectName(u"checkBox_screenshot_jpg")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.checkBox_screenshot_jpg)

        self.checkBox_screenshot_processes = QCheckBox(self.screenshots)
        self.checkBox_screenshot_processes.setObjectName(u"checkBox_screenshot_processes")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.checkBox_screenshot_processes)

        self.checkBox_screenshot_ocr = QCheckBox(self.screenshots)
        self.checkBox_screenshot_ocr.setObjectName(u"checkBox_screenshot_ocr")
        self.checkBox_screenshot_ocr.setEnabled(False)

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.checkBox_screenshot_ocr)

        self.ocr_binary_path = QLineEdit(self.screenshots)
        self.ocr_binary_path.setObjectName(u"ocr_binary_path")
        self.ocr_binary_path.setEnabled(False)

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.ocr_binary_path)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.radioButton_screenshots_qt = QRadioButton(self.screenshots)
        self.radioButton_screenshots_qt.setObjectName(u"radioButton_screenshots_qt")
        self.radioButton_screenshots_qt.setChecked(True)

        self.horizontalLayout_15.addWidget(self.radioButton_screenshots_qt)

        self.radioButton_screenshots_external = QRadioButton(self.screenshots)
        self.radioButton_screenshots_external.setObjectName(u"radioButton_screenshots_external")

        self.horizontalLayout_15.addWidget(self.radioButton_screenshots_external)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_15)


        self.verticalLayout_8.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer)

        self.number_of_screenshots = QLabel(self.screenshots)
        self.number_of_screenshots.setObjectName(u"number_of_screenshots")

        self.verticalLayout_8.addWidget(self.number_of_screenshots)

        self.progressBar = QProgressBar(self.screenshots)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout_8.addWidget(self.progressBar)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.button_start_screenshot = QPushButton(self.screenshots)
        self.button_start_screenshot.setObjectName(u"button_start_screenshot")

        self.horizontalLayout_9.addWidget(self.button_start_screenshot)

        self.button_save_screenshot = QPushButton(self.screenshots)
        self.button_save_screenshot.setObjectName(u"button_save_screenshot")
        self.button_save_screenshot.setEnabled(False)

        self.horizontalLayout_9.addWidget(self.button_save_screenshot)


        self.verticalLayout_8.addLayout(self.horizontalLayout_9)

        self.work.addTab(self.screenshots, "")
        self.splitter.addWidget(self.work)
        self.management = QTabWidget(self.splitter)
        self.management.setObjectName(u"management")
        self.management.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.management.sizePolicy().hasHeightForWidth())
        self.management.setSizePolicy(sizePolicy4)
        self.management.setDocumentMode(False)
        self.management.setTabsClosable(False)
        self.log_tab = QWidget()
        self.log_tab.setObjectName(u"log_tab")
        self.verticalLayout_3 = QVBoxLayout(self.log_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.log_table = QTableView(self.log_tab)
        self.log_table.setObjectName(u"log_table")
        self.log_table.setMinimumSize(QSize(768, 0))
        self.log_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.log_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.log_table.setAutoScroll(False)
        self.log_table.setAlternatingRowColors(True)
        self.log_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.log_table.setSortingEnabled(False)
        self.log_table.horizontalHeader().setCascadingSectionResizes(False)
        self.log_table.horizontalHeader().setStretchLastSection(True)
        self.log_table.verticalHeader().setVisible(False)
        self.log_table.verticalHeader().setCascadingSectionResizes(True)
        self.log_table.verticalHeader().setDefaultSectionSize(30)
        self.log_table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_3.addWidget(self.log_table)

        self.management.addTab(self.log_tab, "")
        self.jobs_tab = QWidget()
        self.jobs_tab.setObjectName(u"jobs_tab")
        self.verticalLayout_2 = QVBoxLayout(self.jobs_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.job_table = QTableView(self.jobs_tab)
        self.job_table.setObjectName(u"job_table")
        self.job_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.job_table.setAlternatingRowColors(True)
        self.job_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.job_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.job_table.setSortingEnabled(False)
        self.job_table.horizontalHeader().setMinimumSectionSize(20)
        self.job_table.horizontalHeader().setStretchLastSection(True)
        self.job_table.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.job_table)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.button_play = QPushButton(self.jobs_tab)
        self.button_play.setObjectName(u"button_play")
        self.button_play.setEnabled(False)
        icon10 = QIcon(QIcon.fromTheme(u"media-playback-start"))
        self.button_play.setIcon(icon10)

        self.horizontalLayout_3.addWidget(self.button_play)

        self.button_pause = QPushButton(self.jobs_tab)
        self.button_pause.setObjectName(u"button_pause")
        self.button_pause.setEnabled(False)
        icon11 = QIcon(QIcon.fromTheme(u"media-playback-pause"))
        self.button_pause.setIcon(icon11)

        self.horizontalLayout_3.addWidget(self.button_pause)

        self.button_stop = QPushButton(self.jobs_tab)
        self.button_stop.setObjectName(u"button_stop")
        self.button_stop.setEnabled(False)
        icon12 = QIcon(QIcon.fromTheme(u"media-playback-stop"))
        self.button_stop.setIcon(icon12)

        self.horizontalLayout_3.addWidget(self.button_stop)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.management.addTab(self.jobs_tab, "")
        self.splitter.addWidget(self.management)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 30))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setObjectName(u"menuOptions")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuOptions.addAction(self.actionEnable_automatic_tools)
        self.menuOptions.addAction(self.actionEnable_automatic_tools_on_import)
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.actionSettings)
        self.menuOptions.addAction(self.actionReload_configuration_from_file)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuEdit.addAction(self.actionSearch_string)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionDelete_hosts_with_no_services)

        self.retranslateUi(MainWindow)
        self.pixel_slider.valueChanged.connect(self.label_slider.setNum)
        self.radioButton_screenshots_external.toggled.connect(self.screenshot_cmd.setEnabled)
        self.checkBox_screenshot_lockscreen.toggled.connect(self.cmd_check_lockscreen.setEnabled)
        self.checkBox_screenshot_lockscreen.toggled.connect(self.cmd_check_result_lockscreen.setEnabled)
        self.checkBox_screenshot_ocr.toggled.connect(self.ocr_binary_path.setEnabled)

        self.work.setCurrentIndex(0)
        self.application_TabWidget.setCurrentIndex(-1)
        self.snippets_tabs.setCurrentIndex(-1)
        self.management.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QtRecon", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"&New", None))
#if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"&Open", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSaveAs.setText(QCoreApplication.translate("MainWindow", u"Sa&ve-as", None))
#if QT_CONFIG(shortcut)
        self.actionSaveAs.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Alt+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"&Exit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"&Settings", None))
#if QT_CONFIG(shortcut)
        self.actionSettings.setShortcut(QCoreApplication.translate("MainWindow", u"F10", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"&About", None))
        self.actionAbout_Qt.setText(QCoreApplication.translate("MainWindow", u"About &Qt", None))
        self.actionTools.setText(QCoreApplication.translate("MainWindow", u"Tools / scripts", None))
        self.actionTools.setIconText(QCoreApplication.translate("MainWindow", u"Tools / scripts", None))
#if QT_CONFIG(tooltip)
        self.actionTools.setToolTip(QCoreApplication.translate("MainWindow", u"Tools / scripts", None))
#endif // QT_CONFIG(tooltip)
        self.actionEnable_automatic_tools.setText(QCoreApplication.translate("MainWindow", u"&Enable automatic tools", None))
        self.actionEnable_automatic_tools_on_import.setText(QCoreApplication.translate("MainWindow", u"Enable automatic tools &on import", None))
        self.actionSearch_string.setText(QCoreApplication.translate("MainWindow", u"Search in notes", None))
#if QT_CONFIG(shortcut)
        self.actionSearch_string.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_running_conf_as_persistent.setText(QCoreApplication.translate("MainWindow", u"Save current configuration", None))
        self.actionReload_configuration_from_file.setText(QCoreApplication.translate("MainWindow", u"&Reload configuration from file", None))
#if QT_CONFIG(shortcut)
        self.actionReload_configuration_from_file.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.actionAutosave_database_every_5_mins.setText(QCoreApplication.translate("MainWindow", u"&Autosave database every 5 mins", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"&Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSet_variables.setText(QCoreApplication.translate("MainWindow", u"&Edit custom variables", None))
        self.actionDelete_hosts_with_no_services.setText(QCoreApplication.translate("MainWindow", u"&Delete hosts with no services", None))
        self.host_list_filter.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search IP or hostname", None))
        self.ImportNmap.setText(QCoreApplication.translate("MainWindow", u"&Import Nmap XML", None))
#if QT_CONFIG(shortcut)
        self.ImportNmap.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+I", None))
#endif // QT_CONFIG(shortcut)
        self.ScanHost.setText(QCoreApplication.translate("MainWindow", u"Scan &host or range", None))
#if QT_CONFIG(shortcut)
        self.ScanHost.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+H", None))
#endif // QT_CONFIG(shortcut)
        self.work.setTabText(self.work.indexOf(self.hosts), QCoreApplication.translate("MainWindow", u"Hosts", None))
        ___qtablewidgetitem = self.port_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"TCP/UDP", None));
        ___qtablewidgetitem1 = self.port_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Ports", None));
        self.machine_list_view_in_host_tab.setText(QCoreApplication.translate("MainWindow", u"Go to host view for this machine", None))
        self.machine_list_copy_selection_to_clipboard.setText(QCoreApplication.translate("MainWindow", u"Copy selected items to clipboard", None))
        self.machine_list_copy_all_to_clipboard.setText(QCoreApplication.translate("MainWindow", u"Copy all items to clipboard", None))
        self.work.setTabText(self.work.indexOf(self.services), QCoreApplication.translate("MainWindow", u"Services", None))
        self.creds_table_filter.setText("")
        self.creds_table_filter.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search string", None))
        self.creds_table_view_in_host_tab.setText(QCoreApplication.translate("MainWindow", u"Go to host view for this machine", None))
        self.creds_table_copy_selection_to_clipboard.setText(QCoreApplication.translate("MainWindow", u"Copy selected items to clipboard", None))
        self.creds_table_copy_all_to_clipboard.setText(QCoreApplication.translate("MainWindow", u"Copy all items to clipboard", None))
        self.work.setTabText(self.work.indexOf(self.creds), QCoreApplication.translate("MainWindow", u"Credentials", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"LHOST", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"LPORT", None))
        self.lport.setInputMask(QCoreApplication.translate("MainWindow", u"99999", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Escape chars", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Urlencode chars", None))
        self.reset_lhost_lport.setText(QCoreApplication.translate("MainWindow", u"Reset values", None))
        self.work.setTabText(self.work.indexOf(self.snippets), QCoreApplication.translate("MainWindow", u"Snippets", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Screenshot source", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Screenshot command (specify output file as %OUTPUT%)", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Temporary working directory", None))
        self.screenshot_work_folder.setText(QCoreApplication.translate("MainWindow", u"/tmp/", None))
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Final directory", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Take screenshot every ", None))
        self.spinBox_screenshots_interval.setSuffix(QCoreApplication.translate("MainWindow", u" seconds", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Number of different pixels required between 2 screenshots :", None))
        self.label_slider.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.checkBox_screenshot_lockscreen.setText(QCoreApplication.translate("MainWindow", u"Don't screenshot if screen is locked", None))
        self.cmd_check_lockscreen.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Command to check if the screen is locked", None))
        self.cmd_check_result_lockscreen.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Expected string in result", None))
        self.checkBox_screenshot_ignore_if_active_window.setText(QCoreApplication.translate("MainWindow", u"Don't screenshot if QtRecon is the active window", None))
        self.checkBox_screenshot_jpg.setText(QCoreApplication.translate("MainWindow", u"Convert images from PNG to JPG", None))
        self.checkBox_screenshot_processes.setText(QCoreApplication.translate("MainWindow", u"Include processes information in a dedicated database", None))
        self.checkBox_screenshot_ocr.setText(QCoreApplication.translate("MainWindow", u"Include OCR information in a database", None))
        self.ocr_binary_path.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Path to OCR binary", None))
        self.radioButton_screenshots_qt.setText(QCoreApplication.translate("MainWindow", u"Native (&X11 only)", None))
        self.radioButton_screenshots_external.setText(QCoreApplication.translate("MainWindow", u"External tool", None))
        self.number_of_screenshots.setText("")
        self.button_start_screenshot.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.button_save_screenshot.setText(QCoreApplication.translate("MainWindow", u"Stop, compress and save to final archive", None))
        self.work.setTabText(self.work.indexOf(self.screenshots), QCoreApplication.translate("MainWindow", u"Screenshots", None))
        self.management.setTabText(self.management.indexOf(self.log_tab), QCoreApplication.translate("MainWindow", u"Logs", None))
        self.button_play.setText("")
        self.button_pause.setText("")
        self.button_stop.setText("")
        self.management.setTabText(self.management.indexOf(self.jobs_tab), QCoreApplication.translate("MainWindow", u"Jobs", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"Fi&le", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"?", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
    # retranslateUi

