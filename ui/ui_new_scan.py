# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_scanVTomiW.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
    QDialogButtonBox, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QSpinBox, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(378, 308)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.target = QLineEdit(Dialog)
        self.target.setObjectName(u"target")

        self.horizontalLayout.addWidget(self.target)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.ports = QLineEdit(Dialog)
        self.ports.setObjectName(u"ports")

        self.horizontalLayout_3.addWidget(self.ports)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.nmap_speed = QSpinBox(Dialog)
        self.nmap_speed.setObjectName(u"nmap_speed")
        self.nmap_speed.setMinimum(0)
        self.nmap_speed.setMaximum(5)
        self.nmap_speed.setValue(3)

        self.horizontalLayout_2.addWidget(self.nmap_speed)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.skip_host_discovery = QCheckBox(Dialog)
        self.skip_host_discovery.setObjectName(u"skip_host_discovery")

        self.verticalLayout.addWidget(self.skip_host_discovery)

        self.check_versions = QCheckBox(Dialog)
        self.check_versions.setObjectName(u"check_versions")
        self.check_versions.setChecked(True)

        self.verticalLayout.addWidget(self.check_versions)

        self.launch_scripts = QCheckBox(Dialog)
        self.launch_scripts.setObjectName(u"launch_scripts")
        self.launch_scripts.setChecked(True)

        self.verticalLayout.addWidget(self.launch_scripts)

        self.os_detection = QCheckBox(Dialog)
        self.os_detection.setObjectName(u"os_detection")
        self.os_detection.setChecked(True)

        self.verticalLayout.addWidget(self.os_detection)

        self.tcp_and_udp = QCheckBox(Dialog)
        self.tcp_and_udp.setObjectName(u"tcp_and_udp")
        self.tcp_and_udp.setChecked(True)

        self.verticalLayout.addWidget(self.tcp_and_udp)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Target", None))
        self.target.setText("")
        self.target.setPlaceholderText(QCoreApplication.translate("Dialog", u"127.0.0.1/32", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Ports", None))
        self.ports.setText(QCoreApplication.translate("Dialog", u"T:-,U:53,161", None))
        self.ports.setPlaceholderText(QCoreApplication.translate("Dialog", u"80,443,8080-8099 or T:1-1024,U:1-200", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Nmap speed", None))
        self.nmap_speed.setPrefix(QCoreApplication.translate("Dialog", u"-T", None))
        self.skip_host_discovery.setText(QCoreApplication.translate("Dialog", u"Skip host discovery (slower)", None))
        self.check_versions.setText(QCoreApplication.translate("Dialog", u"Determine service/version info", None))
        self.launch_scripts.setText(QCoreApplication.translate("Dialog", u"Launch default scripts", None))
        self.os_detection.setText(QCoreApplication.translate("Dialog", u"Enable OS detection (root needed)", None))
        self.tcp_and_udp.setText(QCoreApplication.translate("Dialog", u"Scan both TCP and UDP", None))
    # retranslateUi

