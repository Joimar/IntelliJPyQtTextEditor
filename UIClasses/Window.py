# This Python file uses the following encoding: utf-8

from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtWidgets import QMainWindow, QFileDialog
from urllib.parse import urlparse
import os.path
from UIFiles.UIMainWindow import Ui_MainWindow
from Managers import FileManager


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
        # set __file_changed to True or False
        self.__file_changed = b

    def extractFileName(self, url):
        # extract the file name from the whole path string
        # a = urlparse(url)
        # return os.path.basename(a.path)

        return FileManager.FileManager.extractFileName(self, url)

    def pressFileNew(self):
        # creates new file and cleans plaintext
        print(self.__current_file)
        self.ui.plainTextEdit.clear()
        self.setWindowTitle("Untitled")
        self.__current_file = ""
        self.__setFileChanged(False)

    # Open Functionalities are done
    def pressFileOpen(self):
        # Opens a specific txt file selected by user
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

        self.__setFileChanged(False)

    def pressFileSave(self):
        # save a file or modification when user clicks in save option
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
        self.__setFileChanged(False)

    def closeEvent(self, event):
        # overwritten method to trigger an event when user closes the program
        # calls a dialog asking if user wants to save or discard the changes
        if self.__file_changed == True:
            box = QMessageBox()
            box.setWindowTitle("Program Name")
            box.setText("Do you want to save the changes?")
            box.setStandardButtons(
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

            returnValue = box.exec()
            if returnValue == QMessageBox.StandardButton.Save:
                self.__file_changed = False
                self.pressFileSave()
                event.ignore()

            elif returnValue == QMessageBox.StandardButton.Discard:
                event.accept()
            elif returnValue == QMessageBox.StandardButton.Cancel:
                event.ignore()
