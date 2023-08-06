# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'searchmmLRFU.ui'
##
## Created by: Qt User Interface Compiler version 5.15.9
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
        Dialog.resize(805, 542)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.search_input = QLineEdit(Dialog)
        self.search_input.setObjectName(u"search_input")

        self.horizontalLayout.addWidget(self.search_input)

        self.search_button = QPushButton(Dialog)
        self.search_button.setObjectName(u"search_button")

        self.horizontalLayout.addWidget(self.search_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.host_list = QListWidget(Dialog)
        self.host_list.setObjectName(u"host_list")
        self.host_list.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_3.addWidget(self.host_list)

        self.results = QTextEdit(Dialog)
        self.results.setObjectName(u"results")
        self.results.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.results)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.search_input.setPlaceholderText(QCoreApplication.translate("Dialog", u"Search terms", None))
        self.search_button.setText(QCoreApplication.translate("Dialog", u"Search", None))
    # retranslateUi

