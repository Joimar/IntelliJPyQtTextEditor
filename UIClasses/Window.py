# This Python file uses the following encoding: utf-8
import sys

from PyQt6 import QtWidgets
from PyQt6.QtCore import QFileInfo, QUrl
from PyQt6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog

import os.path
from UIFiles.UIMainWindow import Ui_MainWindow


class MainWindow(QMainWindow):
    current_file = ""

    def __init__(self, parent=None):
        super().__init__(parent)


        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionNew.triggered.connect(self.pressFileNew)

        self.ui.actionSave.triggered.connect(self.pressFileSave)
        self.ui.actionSave.triggered.connect(self.ui.plainTextEdit.textChanged)
        self.ui.actionOpen.triggered.connect(self.pressFileOpen)


    def pressFileNew(self):
        print("Novo arquivo")
        print(self.current_file)

    # Open Functionalities are done
    def pressFileOpen(self):
        file = QFileDialog.getOpenFileName(self, 'Open file', '', 'Text files (*.txt)')
        print(file[0])
        f = open(file[0], "r")
        self.ui.plainTextEdit.setPlainText(f.read())
        f.close()
        self.current_file = file[0]
    def pressFileSave(self):
        print("Save")
        #path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        file = QFileDialog.getOpenFileName(self, 'Saving As')
        print(file)

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
