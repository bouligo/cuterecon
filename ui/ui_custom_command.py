# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'custom_commandYdEOVN.ui'
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
    QDialogButtonBox, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(525, 209)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.command = QLineEdit(Dialog)
        self.command.setObjectName(u"command")

        self.horizontalLayout.addWidget(self.command)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFrameShape(QFrame.NoFrame)
        self.label_2.setLineWidth(2)
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.detached = QCheckBox(Dialog)
        self.detached.setObjectName(u"detached")

        self.verticalLayout.addWidget(self.detached)

        self.in_terminal = QCheckBox(Dialog)
        self.in_terminal.setObjectName(u"in_terminal")
        self.in_terminal.setEnabled(False)

        self.verticalLayout.addWidget(self.in_terminal)

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
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Enter custom command", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Command", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Note: You can use %%%IP%%% or %%%PORT%%% to automaticaly use information from the current selected host", None))
        self.detached.setText(QCoreApplication.translate("Dialog", u"External program", None))
        self.in_terminal.setText(QCoreApplication.translate("Dialog", u"Launch in shell", None))
    # retranslateUi

