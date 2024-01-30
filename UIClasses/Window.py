# This Python file uses the following encoding: utf-8

from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import SIGNAL
from PySide6.QtWidgets import QMainWindow, QFileDialog
import os.path
from UIFiles.UIMainWindow import Ui_MainWindow
from Managers import FileManager


# init

class MainWindow(QMainWindow):
    __current_file = ""
    __file_changed = False
    __saved = False
    __pressedSaved = False
    teste = "Começou"

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionNew.triggered.connect(self.pressFileNew)

        self.ui.actionSave.triggered.connect(self.pressFileSave)
        self.ui.actionSave.triggered.connect(self.ui.plainTextEdit.textChanged)
        self.ui.actionSave_as.triggered.connect(self.pressFileSaveAs)
        self.ui.actionOpen.triggered.connect(self.pressFileOpen)

        self.ui.plainTextEdit.textChanged.connect(self.__setFileChanged)

        self.setWindowTitle("Untitled")

    def __setFileChanged(self):
        # set __file_changed to True or False
        if self.__pressedSaved:
            self.__file_changed = False
            self.__saved = True
            self.__pressedSaved = False
        else:
            self.__file_changed = True
            self.__pressedSaved = False
            self.__saved = False
            self.ui.plainTextEdit.blockSignals(True)
        self.teste = "começou changed"
        print("Digitou")



    def extractFileName(self, url):
        # extract the file name from the whole path string

        return FileManager.FileManager.extractFileName(self, url)

    def pressFileNew(self):
        # creates new file and cleans plaintext
        print(self.__current_file)
        self.ui.plainTextEdit.clear()
        self.setWindowTitle("Untitled")
        self.__current_file = ""
        self.__file_changed = False
        self.__saved = False

    # Open Functionalities are done
    def pressFileOpen(self):
        # Opens a specific txt file selected by user
        self.ui.plainTextEdit.blockSignals(True)
        file = QFileDialog.getOpenFileName(self, 'Open file', '', 'Text files (*.txt)')
        print(file[0])
        print(FileManager.FileManager.extractFileName(self, file[0]))

        if os.path.exists(file[0]):
            self.setWindowTitle(FileManager.FileManager.extractFileName(self, file[0]))
            self.ui.plainTextEdit.clear()
            f = open(file[0], "r")
            self.ui.plainTextEdit.setPlainText(f.read())
            f.close()
            self.__current_file = file[0]
        self.__file_changed = False
        self.__saved = True
        self.ui.plainTextEdit.blockSignals(False)

    def pressFileSave(self):
        # save a file or modification when user clicks in save option
        if FileManager.FileManager.checkFile(self, self.__current_file):
            FileManager.FileManager.updatingFile(self, self.__current_file, self.ui.plainTextEdit.toPlainText())
            self.__pressedSaved = True
            self.ui.plainTextEdit.blockSignals(False)
            print("pressFileSave() FileManager says file exists")
            print(self.__file_changed)
            print(self.__saved)

            self.teste = "Salvou"
            print(self.teste)
        else:
            file = QFileDialog.getSaveFileName(self, 'Saving As', "Document", 'Text files (*.txt)')
            self.__pressedSaved = True
            print(QFileDialog)

            if len(file[0]) > 0:
                print("Selecionado")
                FileManager.FileManager.append(self, file[0], self.ui.plainTextEdit.toPlainText())
                self.setWindowTitle(FileManager.FileManager.extractFileName(self, file[0]))
                self.__file_changed = False
                self.__saved = True
            else:
                print("Não Selecionado")
                self.__saved = False
                self.__file_changed = True
            self.__current_file = file[0]

    def pressFileSaveAs(self):
        # save a file or modification when user clicks in save option
        if FileManager.FileManager.checkFile(self, self.__current_file):
            FileManager.FileManager.updatingFile(self, self.__current_file, self.ui.plainTextEdit.toPlainText())
            self.__pressedSaved = True
            self.ui.plainTextEdit.blockSignals(False)
            print("pressFileSave() FileManager says file exists")
            print(self.__file_changed)
            print(self.__saved)

            self.teste = "Salvou"
            print(self.teste)
        else:
            file = QFileDialog.getSaveFileName(self, 'Saving As', "Document", "All Files (*)")
            self.__pressedSaved = True

            if len(file[0]) > 0:
                print("Selecionado")
                FileManager.FileManager.append(self, file[0], self.ui.plainTextEdit.toPlainText())
                self.setWindowTitle(FileManager.FileManager.extractFileName(self, file[0]))
                self.__file_changed = False
                self.__saved = True
            else:
                print("Não Selecionado")
                self.__saved = False
                self.__file_changed = True
            self.__current_file = file[0]
    def closeEvent(self, event):
        # overwritten method to trigger an event when user closes the program
        # calls a dialog asking if user wants to save or discard the changes

        print(self.__file_changed)
        print(self.__saved)
        print(self.teste)
        if self.__file_changed == True and self.__saved == False:
            box = QMessageBox()
            box.setWindowTitle("Program Name")
            box.setText("Do you want to save the changes?")
            box.setStandardButtons(
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

            returnValue = box.exec()
            if returnValue == QMessageBox.StandardButton.Save:
                self.__file_changed = False
                self.__saved = True
                self.pressFileSave()
                event.accept()

            elif returnValue == QMessageBox.StandardButton.Discard:
                event.accept()
            elif returnValue == QMessageBox.StandardButton.Cancel:
                event.ignore()
