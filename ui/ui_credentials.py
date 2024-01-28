# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'credentialshBDYjq.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QHeaderView, QSizePolicy, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_creds_dialog(object):
    def setupUi(self, creds_dialog):
        if not creds_dialog.objectName():
            creds_dialog.setObjectName(u"creds_dialog")
        creds_dialog.resize(605, 215)
        self.verticalLayout = QVBoxLayout(creds_dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.creds_table = QTableWidget(creds_dialog)
        if (self.creds_table.columnCount() < 4):
            self.creds_table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.creds_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.creds_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.creds_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.creds_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.creds_table.setObjectName(u"creds_table")
        self.creds_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.creds_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.creds_table.horizontalHeader().setStretchLastSection(True)
        self.creds_table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.creds_table)

        self.buttonBox = QDialogButtonBox(creds_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(creds_dialog)
        self.buttonBox.accepted.connect(creds_dialog.accept)
        self.buttonBox.rejected.connect(creds_dialog.reject)

        QMetaObject.connectSlotsByName(creds_dialog)
    # setupUi

    def retranslateUi(self, creds_dialog):
        creds_dialog.setWindowTitle(QCoreApplication.translate("creds_dialog", u"Select credentials to use", None))
        ___qtablewidgetitem = self.creds_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("creds_dialog", u"Type", None));
        ___qtablewidgetitem1 = self.creds_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("creds_dialog", u"Domain", None));
        ___qtablewidgetitem2 = self.creds_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("creds_dialog", u"Username", None));
        ___qtablewidgetitem3 = self.creds_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("creds_dialog", u"Password", None));
    # retranslateUi

