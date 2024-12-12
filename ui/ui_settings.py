# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingslkdniM.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QFrame, QLabel,
    QLineEdit, QScrollArea, QSizePolicy, QSpinBox,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(825, 529)
        icon = QIcon(QIcon.fromTheme(u"preferences-system"))
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabs = QTabWidget(Dialog)
        self.tabs.setObjectName(u"tabs")
        self.tab_paths = QWidget()
        self.tab_paths.setObjectName(u"tab_paths")
        self.verticalLayout_2 = QVBoxLayout(self.tab_paths)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label = QLabel(self.tab_paths)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.nmap_output_dir = QLineEdit(self.tab_paths)
        self.nmap_output_dir.setObjectName(u"nmap_output_dir")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.nmap_output_dir)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.tabs.addTab(self.tab_paths, "")
        self.tab_core_binaries = QWidget()
        self.tab_core_binaries.setObjectName(u"tab_core_binaries")
        self.verticalLayout_3 = QVBoxLayout(self.tab_core_binaries)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_2.setVerticalSpacing(60)
        self.label_2 = QLabel(self.tab_core_binaries)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.core_binaries_nmap_cmd = QLineEdit(self.tab_core_binaries)
        self.core_binaries_nmap_cmd.setObjectName(u"core_binaries_nmap_cmd")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.core_binaries_nmap_cmd)

        self.label_3 = QLabel(self.tab_core_binaries)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.core_binaries_terminal_cmd = QLineEdit(self.tab_core_binaries)
        self.core_binaries_terminal_cmd.setObjectName(u"core_binaries_terminal_cmd")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.core_binaries_terminal_cmd)

        self.label_4 = QLabel(self.tab_core_binaries)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.core_binaries_graphicalsu_cmd = QLineEdit(self.tab_core_binaries)
        self.core_binaries_graphicalsu_cmd.setObjectName(u"core_binaries_graphicalsu_cmd")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.core_binaries_graphicalsu_cmd)


        self.verticalLayout_3.addLayout(self.formLayout_2)

        self.tabs.addTab(self.tab_core_binaries, "")
        self.tab_user_binaries = QWidget()
        self.tab_user_binaries.setObjectName(u"tab_user_binaries")
        self.verticalLayout_4 = QVBoxLayout(self.tab_user_binaries)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tab_user_binaries_scrollArea = QScrollArea(self.tab_user_binaries)
        self.tab_user_binaries_scrollArea.setObjectName(u"tab_user_binaries_scrollArea")
        self.tab_user_binaries_scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.tab_user_binaries_scrollArea.setWidgetResizable(True)
        self.tab_user_binaries_scrollArea_content = QWidget()
        self.tab_user_binaries_scrollArea_content.setObjectName(u"tab_user_binaries_scrollArea_content")
        self.tab_user_binaries_scrollArea_content.setGeometry(QRect(0, 0, 795, 430))
        self.tab_user_binaries_scrollArea_content.setStyleSheet(u"")
        self.tab_user_binaries_scrollArea.setWidget(self.tab_user_binaries_scrollArea_content)

        self.verticalLayout_4.addWidget(self.tab_user_binaries_scrollArea)

        self.tabs.addTab(self.tab_user_binaries, "")
        self.tab_user_preferences = QWidget()
        self.tab_user_preferences.setObjectName(u"tab_user_preferences")
        self.formLayout_4 = QFormLayout(self.tab_user_preferences)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_13 = QLabel(self.tab_user_preferences)
        self.label_13.setObjectName(u"label_13")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_13)

        self.enable_autorun = QCheckBox(self.tab_user_preferences)
        self.enable_autorun.setObjectName(u"enable_autorun")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.enable_autorun)

        self.label_11 = QLabel(self.tab_user_preferences)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_11)

        self.enable_autorun_on_xml_import = QCheckBox(self.tab_user_preferences)
        self.enable_autorun_on_xml_import.setObjectName(u"enable_autorun_on_xml_import")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.enable_autorun_on_xml_import)

        self.label_16 = QLabel(self.tab_user_preferences)
        self.label_16.setObjectName(u"label_16")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.label_16)

        self.confirm_before_tab_removal = QCheckBox(self.tab_user_preferences)
        self.confirm_before_tab_removal.setObjectName(u"confirm_before_tab_removal")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.confirm_before_tab_removal)

        self.label_17 = QLabel(self.tab_user_preferences)
        self.label_17.setObjectName(u"label_17")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.label_17)

        self.dev_null_as_stdin = QCheckBox(self.tab_user_preferences)
        self.dev_null_as_stdin.setObjectName(u"dev_null_as_stdin")

        self.formLayout_4.setWidget(3, QFormLayout.FieldRole, self.dev_null_as_stdin)

        self.label_15 = QLabel(self.tab_user_preferences)
        self.label_15.setObjectName(u"label_15")

        self.formLayout_4.setWidget(4, QFormLayout.LabelRole, self.label_15)

        self.remove_nmap_xml_files_after_scan = QCheckBox(self.tab_user_preferences)
        self.remove_nmap_xml_files_after_scan.setObjectName(u"remove_nmap_xml_files_after_scan")

        self.formLayout_4.setWidget(4, QFormLayout.FieldRole, self.remove_nmap_xml_files_after_scan)

        self.label_18 = QLabel(self.tab_user_preferences)
        self.label_18.setObjectName(u"label_18")

        self.formLayout_4.setWidget(5, QFormLayout.LabelRole, self.label_18)

        self.delete_logs_on_save = QCheckBox(self.tab_user_preferences)
        self.delete_logs_on_save.setObjectName(u"delete_logs_on_save")

        self.formLayout_4.setWidget(5, QFormLayout.FieldRole, self.delete_logs_on_save)

        self.label_12 = QLabel(self.tab_user_preferences)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_4.setWidget(6, QFormLayout.LabelRole, self.label_12)

        self.autosave = QCheckBox(self.tab_user_preferences)
        self.autosave.setObjectName(u"autosave")

        self.formLayout_4.setWidget(6, QFormLayout.FieldRole, self.autosave)

        self.label_20 = QLabel(self.tab_user_preferences)
        self.label_20.setObjectName(u"label_20")

        self.formLayout_4.setWidget(7, QFormLayout.LabelRole, self.label_20)

        self.autosave_interval = QSpinBox(self.tab_user_preferences)
        self.autosave_interval.setObjectName(u"autosave_interval")
        self.autosave_interval.setMinimum(10)
        self.autosave_interval.setMaximum(99999)
        self.autosave_interval.setValue(600)

        self.formLayout_4.setWidget(7, QFormLayout.FieldRole, self.autosave_interval)

        self.label_19 = QLabel(self.tab_user_preferences)
        self.label_19.setObjectName(u"label_19")

        self.formLayout_4.setWidget(9, QFormLayout.LabelRole, self.label_19)

        self.preferred_interfaces = QTextEdit(self.tab_user_preferences)
        self.preferred_interfaces.setObjectName(u"preferred_interfaces")

        self.formLayout_4.setWidget(9, QFormLayout.FieldRole, self.preferred_interfaces)

        self.label_14 = QLabel(self.tab_user_preferences)
        self.label_14.setObjectName(u"label_14")

        self.formLayout_4.setWidget(10, QFormLayout.LabelRole, self.label_14)

        self.preferred_lport = QSpinBox(self.tab_user_preferences)
        self.preferred_lport.setObjectName(u"preferred_lport")
        self.preferred_lport.setMinimum(1)
        self.preferred_lport.setMaximum(65535)
        self.preferred_lport.setValue(4444)

        self.formLayout_4.setWidget(10, QFormLayout.FieldRole, self.preferred_lport)

        self.monospaced_fonts = QLineEdit(self.tab_user_preferences)
        self.monospaced_fonts.setObjectName(u"monospaced_fonts")

        self.formLayout_4.setWidget(8, QFormLayout.FieldRole, self.monospaced_fonts)

        self.label_5 = QLabel(self.tab_user_preferences)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_4.setWidget(8, QFormLayout.LabelRole, self.label_5)

        self.tabs.addTab(self.tab_user_preferences, "")
        self.tab_user_variables = QWidget()
        self.tab_user_variables.setObjectName(u"tab_user_variables")
        self.tab_user_variables_layout = QVBoxLayout(self.tab_user_variables)
        self.tab_user_variables_layout.setObjectName(u"tab_user_variables_layout")
        self.tab_user_variables_scrollArea = QScrollArea(self.tab_user_variables)
        self.tab_user_variables_scrollArea.setObjectName(u"tab_user_variables_scrollArea")
        self.tab_user_variables_scrollArea.setWidgetResizable(True)
        self.tab_user_variables_scrollArea_content = QWidget()
        self.tab_user_variables_scrollArea_content.setObjectName(u"tab_user_variables_scrollArea_content")
        self.tab_user_variables_scrollArea_content.setGeometry(QRect(0, 0, 795, 430))
        self.tab_user_variables_scrollArea.setWidget(self.tab_user_variables_scrollArea_content)

        self.tab_user_variables_layout.addWidget(self.tab_user_variables_scrollArea)

        self.tabs.addTab(self.tab_user_variables, "")
        self.tab_snippets = QWidget()
        self.tab_snippets.setObjectName(u"tab_snippets")
        self.verticalLayout_5 = QVBoxLayout(self.tab_snippets)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.snippets_content = QTextEdit(self.tab_snippets)
        self.snippets_content.setObjectName(u"snippets_content")

        self.verticalLayout_5.addWidget(self.snippets_content)

        self.tabs.addTab(self.tab_snippets, "")

        self.verticalLayout.addWidget(self.tabs)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Settings", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Nmap output directory", None))
        self.nmap_output_dir.setPlaceholderText(QCoreApplication.translate("Dialog", u"/tmp/QtRecon", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_paths), QCoreApplication.translate("Dialog", u"Paths", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Nmap default command prefix", None))
        self.core_binaries_nmap_cmd.setPlaceholderText(QCoreApplication.translate("Dialog", u"/usr/bin/nmap -v --min-rate 500", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Terminal default command prefix", None))
        self.core_binaries_terminal_cmd.setPlaceholderText(QCoreApplication.translate("Dialog", u"/usr/bin/konsole -e", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Graphical SU default command prefix", None))
        self.core_binaries_graphicalsu_cmd.setPlaceholderText(QCoreApplication.translate("Dialog", u"/usr/bin/pkexec", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_core_binaries), QCoreApplication.translate("Dialog", u"Core binaries", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_user_binaries), QCoreApplication.translate("Dialog", u"User binaries", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Enable autorun for scanned services", None))
        self.enable_autorun.setText("")
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Enable autorun on XML import", None))
        self.enable_autorun_on_xml_import.setText("")
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Confirm before tab removal", None))
        self.confirm_before_tab_removal.setText("")
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Use /dev/null as stdin for programs", None))
        self.dev_null_as_stdin.setText("")
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Remove nmap XML files after scanning", None))
        self.remove_nmap_xml_files_after_scan.setText("")
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Delete logs on workspace save", None))
        self.delete_logs_on_save.setText("")
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Autosave QtRecon database", None))
        self.autosave.setText("")
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Autosave interval (in secs)", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Preferred network interfaces for LHOST", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Preferred LPORT", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"List of monospaced fonts (comma separated)", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_user_preferences), QCoreApplication.translate("Dialog", u"User preferences", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_user_variables), QCoreApplication.translate("Dialog", u"User variables", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_snippets), QCoreApplication.translate("Dialog", u"Snippets", None))
    # retranslateUi

