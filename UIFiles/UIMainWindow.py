# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UIMainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QMenu,
    QMenuBar, QPlainTextEdit, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(920, 600)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_as = QAction(MainWindow)
        self.actionSave_as.setObjectName(u"actionSave_as")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        self.actionSet_Dark_Mode = QAction(MainWindow)
        self.actionSet_Dark_Mode.setObjectName(u"actionSet_Dark_Mode")
        self.actionSet_Light_Mode = QAction(MainWindow)
        self.actionSet_Light_Mode.setObjectName(u"actionSet_Light_Mode")
        self.actionChange_Font_Size = QAction(MainWindow)
        self.actionChange_Font_Size.setObjectName(u"actionChange_Font_Size")
        self.actionPrint = QAction(MainWindow)
        self.actionPrint.setObjectName(u"actionPrint")
        self.actionExport_PDF = QAction(MainWindow)
        self.actionExport_PDF.setObjectName(u"actionExport_PDF")
        self.actionpt = QAction(MainWindow)
        self.actionpt.setObjectName(u"actionpt")
        self.actiones = QAction(MainWindow)
        self.actiones.setObjectName(u"actiones")
        self.actionfr = QAction(MainWindow)
        self.actionfr.setObjectName(u"actionfr")
        self.actionde = QAction(MainWindow)
        self.actionde.setObjectName(u"actionde")
        self.actionen = QAction(MainWindow)
        self.actionen.setObjectName(u"actionen")
        self.actionru = QAction(MainWindow)
        self.actionru.setObjectName(u"actionru")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 920, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuAppearance = QMenu(self.menubar)
        self.menuAppearance.setObjectName(u"menuAppearance")
        self.menuLanguage = QMenu(self.menubar)
        self.menuLanguage.setObjectName(u"menuLanguage")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuAppearance.menuAction())
        self.menubar.addAction(self.menuLanguage.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_PDF)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuAppearance.addAction(self.actionSet_Dark_Mode)
        self.menuAppearance.addAction(self.actionSet_Light_Mode)
        self.menuAppearance.addSeparator()
        self.menuAppearance.addAction(self.actionChange_Font_Size)
        self.menuLanguage.addAction(self.actionpt)
        self.menuLanguage.addAction(self.actiones)
        self.menuLanguage.addAction(self.actionfr)
        self.menuLanguage.addAction(self.actionde)
        self.menuLanguage.addAction(self.actionen)
        self.menuLanguage.addAction(self.actionru)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_as.setText(QCoreApplication.translate("MainWindow", u"Save as", None))
#if QT_CONFIG(shortcut)
        self.actionSave_as.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
#if QT_CONFIG(shortcut)
        self.actionUndo.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
#if QT_CONFIG(shortcut)
        self.actionRedo.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Y", None))
#endif // QT_CONFIG(shortcut)
        self.actionSet_Dark_Mode.setText(QCoreApplication.translate("MainWindow", u"Set Dark Mode", None))
        self.actionSet_Light_Mode.setText(QCoreApplication.translate("MainWindow", u"Set Light Mode", None))
        self.actionChange_Font_Size.setText(QCoreApplication.translate("MainWindow", u"Change Font Size", None))
        self.actionPrint.setText(QCoreApplication.translate("MainWindow", u"Print", None))
#if QT_CONFIG(shortcut)
        self.actionPrint.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
        self.actionExport_PDF.setText(QCoreApplication.translate("MainWindow", u"Export PDF", None))
        self.actionpt.setText(QCoreApplication.translate("MainWindow", u"pt", None))
        self.actiones.setText(QCoreApplication.translate("MainWindow", u"es", None))
        self.actionfr.setText(QCoreApplication.translate("MainWindow", u"fr", None))
        self.actionde.setText(QCoreApplication.translate("MainWindow", u"de", None))
        self.actionen.setText(QCoreApplication.translate("MainWindow", u"en", None))
        self.actionru.setText(QCoreApplication.translate("MainWindow", u"ru", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuAppearance.setTitle(QCoreApplication.translate("MainWindow", u"Appearance", None))
        self.menuLanguage.setTitle(QCoreApplication.translate("MainWindow", u"Language", None))
    # retranslateUi

