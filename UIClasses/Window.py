# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
import os.path
from UIFiles.UIMainWindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionNew.triggered.connect(self.pressFileNew)
        self.ui.menuFile.triggered.connect(self.pressFile)
        self.ui.actionSave.triggered.connect(self.saveFile)
        self.ui.actionSave.triggered.connect(self.ui.plainTextEdit.textChanged)

    def pressFileNew(self):
        print("Novo arquivo")

    def pressFile(self):
        print("File")

    def pressFileSave(filename):
        print("Save")

    def saveFile(self):
        check_file = os.path.isfile("myfile.txt")
        if check_file:
            f = open("myfile.txt", "w")
            f.write(self.ui.plainTextEdit.toPlainText())
            f.close()
        else:
            f = open("myfile.txt", "x")
            f.write(self.ui.plainTextEdit.toPlainText())
            f.close()

