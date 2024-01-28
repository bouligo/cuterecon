# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'abouteiYJRG.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

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
        self.image.setPixmap(QPixmap(u"icons/icon.ico"))

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

