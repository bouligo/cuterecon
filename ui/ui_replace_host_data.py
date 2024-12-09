# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'replace_host_dataXNeotS.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_replace_host_data(object):
    def setupUi(self, replace_host_data):
        if not replace_host_data.objectName():
            replace_host_data.setObjectName(u"replace_host_data")
        replace_host_data.setWindowModality(Qt.WindowModality.ApplicationModal)
        replace_host_data.resize(716, 112)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(replace_host_data.sizePolicy().hasHeightForWidth())
        replace_host_data.setSizePolicy(sizePolicy)
        replace_host_data.setMinimumSize(QSize(716, 112))
        replace_host_data.setMaximumSize(QSize(716, 112))
        replace_host_data.setModal(True)
        self.verticalLayout = QVBoxLayout(replace_host_data)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.text = QLabel(replace_host_data)
        self.text.setObjectName(u"text")
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.text)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.merge = QPushButton(replace_host_data)
        self.merge.setObjectName(u"merge")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.merge.setIcon(icon)

        self.gridLayout.addWidget(self.merge, 0, 0, 1, 1)

        self.erase = QPushButton(replace_host_data)
        self.erase.setObjectName(u"erase")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSaveAs))
        self.erase.setIcon(icon1)

        self.gridLayout.addWidget(self.erase, 0, 1, 1, 1)

        self.keep = QPushButton(replace_host_data)
        self.keep.setObjectName(u"keep")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
        self.keep.setIcon(icon2)

        self.gridLayout.addWidget(self.keep, 0, 2, 1, 1)

        self.merge_all = QPushButton(replace_host_data)
        self.merge_all.setObjectName(u"merge_all")
        self.merge_all.setIcon(icon)

        self.gridLayout.addWidget(self.merge_all, 1, 0, 1, 1)

        self.erase_all = QPushButton(replace_host_data)
        self.erase_all.setObjectName(u"erase_all")
        self.erase_all.setIcon(icon1)

        self.gridLayout.addWidget(self.erase_all, 1, 1, 1, 1)

        self.keep_all = QPushButton(replace_host_data)
        self.keep_all.setObjectName(u"keep_all")
        self.keep_all.setIcon(icon2)

        self.gridLayout.addWidget(self.keep_all, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(replace_host_data)

        QMetaObject.connectSlotsByName(replace_host_data)
    # setupUi

    def retranslateUi(self, replace_host_data):
        replace_host_data.setWindowTitle(QCoreApplication.translate("replace_host_data", u"Host already exists in database", None))
        self.text.setText("")
        self.merge.setText(QCoreApplication.translate("replace_host_data", u"Merge with previous open ports", None))
        self.erase.setText(QCoreApplication.translate("replace_host_data", u"Replace old data with new data", None))
        self.keep.setText(QCoreApplication.translate("replace_host_data", u"Discard new data", None))
        self.merge_all.setText(QCoreApplication.translate("replace_host_data", u"Merge all hosts with previous open ports", None))
        self.erase_all.setText(QCoreApplication.translate("replace_host_data", u"Replace all old data with new data", None))
        self.keep_all.setText(QCoreApplication.translate("replace_host_data", u"Discard all new data", None))
    # retranslateUi

