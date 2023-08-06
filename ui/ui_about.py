# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'aboutyjxvlr.ui'
##
## Created by: Qt User Interface Compiler version 5.15.10
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(454, 260)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.image = QLabel(Dialog)
        self.image.setObjectName(u"image")

        self.horizontalLayout.addWidget(self.image)

        self.text = QLabel(Dialog)
        self.text.setObjectName(u"text")

        self.horizontalLayout.addWidget(self.text)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.button = QPushButton(Dialog)
        self.button.setObjectName(u"button")

        self.verticalLayout.addWidget(self.button)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.image.setText("")
        self.text.setText("")
        self.button.setText(QCoreApplication.translate("Dialog", u"Ok", None))
    # retranslateUi

