# This Python file uses the following encoding: utf-8
import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QPushButton
from PySide6.QtWidgets import QMainWindow, QFileDialog
from urllib.parse import urlparse
import os.path
from UIFiles.UIMainWindow import Ui_MainWindow
from PyQt6.QtGui import QSyntaxHighlighter


class MainWindow(QMainWindow):
    __current_file = ""
    __file_changed = False

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionNew.triggered.connect(self.pressFileNew)

        self.ui.actionSave.triggered.connect(self.pressFileSave)
        self.ui.actionSave.triggered.connect(self.ui.plainTextEdit.textChanged)
        self.ui.actionOpen.triggered.connect(self.pressFileOpen)

        self.ui.plainTextEdit.textChanged.connect(lambda: self.__setFileChanged(True))

        self.setWindowTitle("Untitled")

    def __setFileChanged(self, b):
        self.__file_changed = b
        print("Modificação")

    def extractFileName(self, url):
        a = urlparse(url)
        return os.path.basename(a.path)

    def pressFileNew(self):
        print("Novo arquivo")
        print(self.__current_file)
        self.ui.plainTextEdit.clear()
        self.setWindowTitle("Untitled")
        self.__current_file = ""

    # Open Functionalities are done
    def pressFileOpen(self):
        file = QFileDialog.getOpenFileName(self, 'Open file', '', 'Text files (*.txt)')
        print(file[0])
        print(self.extractFileName(file[0]))

        if os.path.exists(file[0]):
            self.setWindowTitle(self.extractFileName(file[0]))
            self.ui.plainTextEdit.clear()
            f = open(file[0], "r")
            self.ui.plainTextEdit.setPlainText(f.read())
            f.close()
            self.__current_file = file[0]
            print("current file: " + self.__current_file)

    def pressFileSave(self):
        print("Save")
        check_file = os.path.isfile(self.__current_file)

        if check_file:
            f = open(self.__current_file, "r+")
            f.truncate(0)
            f.write(self.ui.plainTextEdit.toPlainText())
            f.close()
        else:
            file = QFileDialog.getSaveFileName(self, 'Saving As', "Document", 'Text files (*.txt)')
            if len(file[0]) > 0:
                f = open(file[0], "a")
                f.write(self.ui.plainTextEdit.toPlainText())
                f.close()
                self.setWindowTitle(self.extractFileName(file[0]))
            self.__current_file = file[0]

    def closeEvent(self, event):
        print("Closing Window Event")
        if self.__file_changed == True:
            print("Salvando")
            box = QMessageBox()
            box.setWindowTitle("Fechando")
            box.setText("TEXTO")
            box.setStandardButtons(
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

            returnValue = box.exec()
            print("Current File" + self.__current_file)
            if returnValue == QMessageBox.StandardButton.Save:
                print("Salvar")
                self.__file_changed = False
                self.pressFileSave()
                event.ignore()

            elif returnValue == QMessageBox.StandardButton.Discard:
                print("Descartar")
                event.accept()
            elif returnValue == QMessageBox.StandardButton.Cancel:
                print("Cancelar")
                event.ignore()



