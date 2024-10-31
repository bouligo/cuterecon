# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_scanXHlPFB.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QFormLayout, QLabel,
    QLineEdit, QSizePolicy, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(498, 406)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.target = QLineEdit(Dialog)
        self.target.setObjectName(u"target")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.target)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.ports = QLineEdit(Dialog)
        self.ports.setObjectName(u"ports")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ports)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.type = QComboBox(Dialog)
        icon = QIcon(QIcon.fromTheme(u"dialog-password"))
        self.type.addItem(icon, "")
        self.type.addItem("")
        self.type.addItem(icon, "")
        self.type.addItem(icon, "")
        self.type.addItem(icon, "")
        self.type.addItem(icon, "")
        self.type.addItem(icon, "")
        self.type.addItem(icon, "")
        self.type.setObjectName(u"type")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.type)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_2)

        self.nmap_speed = QSpinBox(Dialog)
        self.nmap_speed.setObjectName(u"nmap_speed")
        self.nmap_speed.setMinimum(0)
        self.nmap_speed.setMaximum(5)
        self.nmap_speed.setValue(3)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.nmap_speed)

        self.skip_host_discovery = QCheckBox(Dialog)
        self.skip_host_discovery.setObjectName(u"skip_host_discovery")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.skip_host_discovery)

        self.check_versions = QCheckBox(Dialog)
        self.check_versions.setObjectName(u"check_versions")
        self.check_versions.setChecked(True)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.check_versions)

        self.launch_scripts = QCheckBox(Dialog)
        self.launch_scripts.setObjectName(u"launch_scripts")
        self.launch_scripts.setChecked(True)

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.launch_scripts)

        self.os_detection = QCheckBox(Dialog)
        self.os_detection.setObjectName(u"os_detection")
        self.os_detection.setIcon(icon)
        self.os_detection.setChecked(True)

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.os_detection)

        self.tcp_and_udp = QCheckBox(Dialog)
        self.tcp_and_udp.setObjectName(u"tcp_and_udp")
        self.tcp_and_udp.setIcon(icon)
        self.tcp_and_udp.setChecked(True)

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.tcp_and_udp)

        self.save_as_default = QCheckBox(Dialog)
        self.save_as_default.setObjectName(u"save_as_default")

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.save_as_default)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.additional_args = QLineEdit(Dialog)
        self.additional_args.setObjectName(u"additional_args")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.additional_args)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"New scan", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Target", None))
        self.target.setText("")
        self.target.setPlaceholderText(QCoreApplication.translate("Dialog", u"127.0.0.1/32", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Ports", None))
        self.ports.setText("")
        self.ports.setPlaceholderText(QCoreApplication.translate("Dialog", u"80,443,8080-8099 or T:1-1024,U:1-200", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Scan type", None))
        self.type.setItemText(0, QCoreApplication.translate("Dialog", u"Syn scan (-sS)", None))
        self.type.setItemText(1, QCoreApplication.translate("Dialog", u"Connect scan (-sT)", None))
        self.type.setItemText(2, QCoreApplication.translate("Dialog", u"ACK scan (-sA)", None))
        self.type.setItemText(3, QCoreApplication.translate("Dialog", u"Window scan (-sW)", None))
        self.type.setItemText(4, QCoreApplication.translate("Dialog", u"Maimon scan (-sM)", None))
        self.type.setItemText(5, QCoreApplication.translate("Dialog", u"Null scan (-sN)", None))
        self.type.setItemText(6, QCoreApplication.translate("Dialog", u"FIN scan (-sF)", None))
        self.type.setItemText(7, QCoreApplication.translate("Dialog", u"Xmas scan (-sX)", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Nmap speed", None))
        self.nmap_speed.setPrefix(QCoreApplication.translate("Dialog", u"-T", None))
        self.skip_host_discovery.setText(QCoreApplication.translate("Dialog", u"Skip host discovery (slower)", None))
        self.check_versions.setText(QCoreApplication.translate("Dialog", u"Determine service/version info", None))
        self.launch_scripts.setText(QCoreApplication.translate("Dialog", u"Launch default scripts", None))
        self.os_detection.setText(QCoreApplication.translate("Dialog", u"(root needed) Enable OS detection", None))
        self.tcp_and_udp.setText(QCoreApplication.translate("Dialog", u"(root needed) Scan both TCP and UDP", None))
        self.save_as_default.setText(QCoreApplication.translate("Dialog", u"Save as default configuration for future scans", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Additional args", None))
        self.additional_args.setText("")
        self.additional_args.setPlaceholderText(QCoreApplication.translate("Dialog", u"Optional", None))
    # retranslateUi

