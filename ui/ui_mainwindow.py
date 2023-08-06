# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowRQgMhy.ui'
##
## Created by: Qt User Interface Compiler version 5.15.10
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 755)
        MainWindow.setLayoutDirection(Qt.LeftToRight)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionNew.setEnabled(True)
        icon = QIcon()
        iconThemeName = u"document-new"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.actionNew.setIcon(icon)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionOpen.setEnabled(True)
        icon1 = QIcon()
        iconThemeName = u"document-open"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.actionOpen.setIcon(icon1)
        self.actionSaveAs = QAction(MainWindow)
        self.actionSaveAs.setObjectName(u"actionSaveAs")
        self.actionSaveAs.setEnabled(True)
        icon2 = QIcon()
        iconThemeName = u"document-save"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.actionSaveAs.setIcon(icon2)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        icon3 = QIcon()
        iconThemeName = u"application-exit"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.actionExit.setIcon(icon3)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionSettings.setEnabled(False)
        icon4 = QIcon()
        iconThemeName = u"preferences-system"
        if QIcon.hasThemeIcon(iconThemeName):
            icon4 = QIcon.fromTheme(iconThemeName)
        else:
            icon4.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.actionSettings.setIcon(icon4)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        icon5 = QIcon()
        iconThemeName = u"help-about"
        if QIcon.hasThemeIcon(iconThemeName):
            icon5 = QIcon.fromTheme(iconThemeName)
        else:
            icon5.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.actionAbout.setIcon(icon5)
        self.actionAbout_Qt = QAction(MainWindow)
        self.actionAbout_Qt.setObjectName(u"actionAbout_Qt")
        self.actionTools = QAction(MainWindow)
        self.actionTools.setObjectName(u"actionTools")
        self.actionTools.setEnabled(False)
        icon6 = QIcon()
        iconThemeName = u"applications-utilities"
        if QIcon.hasThemeIcon(iconThemeName):
            icon6 = QIcon.fromTheme(iconThemeName)
        else:
            icon6.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.actionTools.setIcon(icon6)
        self.actionEnable_automatic_tools = QAction(MainWindow)
        self.actionEnable_automatic_tools.setObjectName(u"actionEnable_automatic_tools")
        self.actionEnable_automatic_tools.setCheckable(True)
        self.actionEnable_automatic_tools.setChecked(True)
        self.actionEnable_automatic_tools_on_import = QAction(MainWindow)
        self.actionEnable_automatic_tools_on_import.setObjectName(u"actionEnable_automatic_tools_on_import")
        self.actionEnable_automatic_tools_on_import.setCheckable(True)
        self.actionEnable_automatic_tools_on_import.setChecked(False)
        self.actionSet_variables = QAction(MainWindow)
        self.actionSet_variables.setObjectName(u"actionSet_variables")
        icon7 = QIcon()
        iconThemeName = u"list-add"
        if QIcon.hasThemeIcon(iconThemeName):
            icon7 = QIcon.fromTheme(iconThemeName)
        else:
            icon7.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.actionSet_variables.setIcon(icon7)
        self.actionSearch_string = QAction(MainWindow)
        self.actionSearch_string.setObjectName(u"actionSearch_string")
        self.actionSearch_string.setEnabled(True)
        icon8 = QIcon()
        iconThemeName = u"edit-find"
        if QIcon.hasThemeIcon(iconThemeName):
            icon8 = QIcon.fromTheme(iconThemeName)
        else:
            icon8.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.actionSearch_string.setIcon(icon8)
        self.actionSave_running_conf_as_persistent = QAction(MainWindow)
        self.actionSave_running_conf_as_persistent.setObjectName(u"actionSave_running_conf_as_persistent")
        self.actionSave_running_conf_as_persistent.setEnabled(False)
        self.actionReload_configuration_from_file = QAction(MainWindow)
        self.actionReload_configuration_from_file.setObjectName(u"actionReload_configuration_from_file")
        self.actionAutosave_database_every_5_mins = QAction(MainWindow)
        self.actionAutosave_database_every_5_mins.setObjectName(u"actionAutosave_database_every_5_mins")
        self.actionAutosave_database_every_5_mins.setCheckable(True)
        self.actionAutosave_database_every_5_mins.setEnabled(False)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        icon9 = QIcon(QIcon.fromTheme(u"document-save"))
        self.actionSave.setIcon(icon9)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.work = QTabWidget(self.splitter)
        self.work.setObjectName(u"work")
        self.work.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
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
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.host_list = QTableView(self.layoutWidget)
        self.host_list.setObjectName(u"host_list")
        font = QFont()
        font.setPointSize(12)
        self.host_list.setFont(font)
        self.host_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.host_list.setAlternatingRowColors(True)
        self.host_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.host_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.host_list.setGridStyle(Qt.DashLine)
        self.host_list.horizontalHeader().setMinimumSectionSize(10)
        self.host_list.horizontalHeader().setStretchLastSection(True)
        self.host_list.verticalHeader().setVisible(False)

        self.verticalLayout_5.addWidget(self.host_list)

        self.searchbox = QLineEdit(self.layoutWidget)
        self.searchbox.setObjectName(u"searchbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.searchbox.sizePolicy().hasHeightForWidth())
        self.searchbox.setSizePolicy(sizePolicy1)

        self.verticalLayout_5.addWidget(self.searchbox)

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
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
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
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.port_table.sizePolicy().hasHeightForWidth())
        self.port_table.setSizePolicy(sizePolicy3)
        self.port_table.setFont(font)
        self.port_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.port_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.port_table.horizontalHeader().setStretchLastSection(True)
        self.port_table.verticalHeader().setVisible(False)

        self.horizontalLayout_2.addWidget(self.port_table)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.hosts_for_port_table = QTableView(self.services)
        self.hosts_for_port_table.setObjectName(u"hosts_for_port_table")
        self.hosts_for_port_table.setFont(font)
        self.hosts_for_port_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.hosts_for_port_table.setAlternatingRowColors(True)
        self.hosts_for_port_table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.hosts_for_port_table.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_6.addWidget(self.hosts_for_port_table)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.machine_list_copy_selection_to_clipboard = QPushButton(self.services)
        self.machine_list_copy_selection_to_clipboard.setObjectName(u"machine_list_copy_selection_to_clipboard")
        icon10 = QIcon()
        iconThemeName = u"edit-copy"
        if QIcon.hasThemeIcon(iconThemeName):
            icon10 = QIcon.fromTheme(iconThemeName)
        else:
            icon10.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.machine_list_copy_selection_to_clipboard.setIcon(icon10)

        self.horizontalLayout_7.addWidget(self.machine_list_copy_selection_to_clipboard)

        self.machine_list_copy_all_to_clipboard = QPushButton(self.services)
        self.machine_list_copy_all_to_clipboard.setObjectName(u"machine_list_copy_all_to_clipboard")
        self.machine_list_copy_all_to_clipboard.setIcon(icon10)

        self.horizontalLayout_7.addWidget(self.machine_list_copy_all_to_clipboard)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        self.work.addTab(self.services, "")
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

        self.label_3 = QLabel(self.snippets)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.sharename = QLineEdit(self.snippets)
        self.sharename.setObjectName(u"sharename")

        self.horizontalLayout_4.addWidget(self.sharename)

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
        self.splitter.addWidget(self.work)
        self.management = QTabWidget(self.splitter)
        self.management.setObjectName(u"management")
        self.management.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        self.log_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.log_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.log_table.setAutoScroll(False)
        self.log_table.setAlternatingRowColors(True)
        self.log_table.setSelectionBehavior(QAbstractItemView.SelectRows)
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
        self.job_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.job_table.setAlternatingRowColors(True)
        self.job_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.job_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.job_table.setSortingEnabled(False)
        self.job_table.horizontalHeader().setMinimumSectionSize(20)
        self.job_table.horizontalHeader().setStretchLastSection(True)
        self.job_table.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.job_table)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.button_play = QPushButton(self.jobs_tab)
        self.button_play.setObjectName(u"button_play")
        self.button_play.setEnabled(False)
        icon11 = QIcon()
        iconThemeName = u"media-playback-start"
        if QIcon.hasThemeIcon(iconThemeName):
            icon11 = QIcon.fromTheme(iconThemeName)
        else:
            icon11.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.button_play.setIcon(icon11)

        self.horizontalLayout_3.addWidget(self.button_play)

        self.button_pause = QPushButton(self.jobs_tab)
        self.button_pause.setObjectName(u"button_pause")
        self.button_pause.setEnabled(False)
        icon12 = QIcon()
        iconThemeName = u"media-playback-pause"
        if QIcon.hasThemeIcon(iconThemeName):
            icon12 = QIcon.fromTheme(iconThemeName)
        else:
            icon12.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.button_pause.setIcon(icon12)

        self.horizontalLayout_3.addWidget(self.button_pause)

        self.button_stop = QPushButton(self.jobs_tab)
        self.button_stop.setObjectName(u"button_stop")
        self.button_stop.setEnabled(False)
        icon13 = QIcon()
        iconThemeName = u"media-playback-stop"
        if QIcon.hasThemeIcon(iconThemeName):
            icon13 = QIcon.fromTheme(iconThemeName)
        else:
            icon13.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.button_stop.setIcon(icon13)

        self.horizontalLayout_3.addWidget(self.button_stop)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.management.addTab(self.jobs_tab, "")
        self.splitter.addWidget(self.management)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 30))
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
        self.menuOptions.addAction(self.actionAutosave_database_every_5_mins)
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.actionTools)
        self.menuOptions.addAction(self.actionSettings)
        self.menuOptions.addAction(self.actionReload_configuration_from_file)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuEdit.addAction(self.actionSet_variables)
        self.menuEdit.addAction(self.actionSearch_string)

        self.retranslateUi(MainWindow)

        self.work.setCurrentIndex(0)
        self.application_TabWidget.setCurrentIndex(-1)
        self.snippets_tabs.setCurrentIndex(-1)
        self.management.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QtRecon", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSaveAs.setText(QCoreApplication.translate("MainWindow", u"Save-as", None))
#if QT_CONFIG(shortcut)
        self.actionSaveAs.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Alt+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionAbout_Qt.setText(QCoreApplication.translate("MainWindow", u"About Qt", None))
        self.actionTools.setText(QCoreApplication.translate("MainWindow", u"Tools / scripts", None))
        self.actionTools.setIconText(QCoreApplication.translate("MainWindow", u"Tools / scripts", None))
#if QT_CONFIG(tooltip)
        self.actionTools.setToolTip(QCoreApplication.translate("MainWindow", u"Tools / scripts", None))
#endif // QT_CONFIG(tooltip)
        self.actionEnable_automatic_tools.setText(QCoreApplication.translate("MainWindow", u"Enable automatic tools", None))
        self.actionEnable_automatic_tools_on_import.setText(QCoreApplication.translate("MainWindow", u"Enable automatic tools on import", None))
        self.actionSet_variables.setText(QCoreApplication.translate("MainWindow", u"Set variables", None))
        self.actionSearch_string.setText(QCoreApplication.translate("MainWindow", u"Search string", None))
#if QT_CONFIG(shortcut)
        self.actionSearch_string.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_running_conf_as_persistent.setText(QCoreApplication.translate("MainWindow", u"Save current configuration", None))
        self.actionReload_configuration_from_file.setText(QCoreApplication.translate("MainWindow", u"Reload configuration from file", None))
        self.actionAutosave_database_every_5_mins.setText(QCoreApplication.translate("MainWindow", u"Autosave database every 5 mins", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.searchbox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search IP or hostname", None))
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
        self.machine_list_copy_selection_to_clipboard.setText(QCoreApplication.translate("MainWindow", u"Copy selected items to clipboard", None))
        self.machine_list_copy_all_to_clipboard.setText(QCoreApplication.translate("MainWindow", u"Copy all items to clipboard", None))
        self.work.setTabText(self.work.indexOf(self.services), QCoreApplication.translate("MainWindow", u"Services", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"LHOST", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"LPORT", None))
        self.lport.setInputMask(QCoreApplication.translate("MainWindow", u"99999", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"SMB Sharename", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Escape chars", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Urlencode chars", None))
        self.reset_lhost_lport.setText(QCoreApplication.translate("MainWindow", u"Reset values", None))
        self.work.setTabText(self.work.indexOf(self.snippets), QCoreApplication.translate("MainWindow", u"Snippets", None))
        self.management.setTabText(self.management.indexOf(self.log_tab), QCoreApplication.translate("MainWindow", u"Logs", None))
        self.button_play.setText("")
        self.button_pause.setText("")
        self.button_stop.setText("")
        self.management.setTabText(self.management.indexOf(self.jobs_tab), QCoreApplication.translate("MainWindow", u"Jobs", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"?", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
    # retranslateUi

