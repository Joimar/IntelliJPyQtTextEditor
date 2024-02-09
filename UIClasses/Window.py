# This Python file uses the following encoding: utf-8

from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtWidgets import QMainWindow, QFileDialog
import os.path
from UIFiles.UIMainWindow import Ui_MainWindow
from Managers import FileManager


class MainWindow(QMainWindow):
    __current_file = ""
    __file_changed = False
    __saved = False
    __pressedSaved = False

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # File Actions
        self.ui.actionNew.triggered.connect(self.pressFileNew)
        self.ui.actionSave.triggered.connect(self.pressFileSave)
        self.ui.actionSave.triggered.connect(self.ui.plainTextEdit.textChanged)
        self.ui.actionSave_as.triggered.connect(self.pressFileSaveAs)
        self.ui.actionOpen.triggered.connect(self.pressFileOpen)
        # Edit Actions
        self.ui.actionUndo.triggered.connect(self.pressEditUndo)
        self.ui.actionRedo.triggered.connect(self.pressEditRedo)

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
            # check if file already exists. If so, program is handling with an opened file and not a just created one
            FileManager.FileManager.updatingFile(self, self.__current_file, self.ui.plainTextEdit.toPlainText())
            self.__pressedSaved = True
            self.ui.plainTextEdit.blockSignals(False)
        else:
            self.pressFileSaveAs()

    def pressFileSaveAs(self):
        # save a file or modification when user clicks in save option
        file = QFileDialog.getSaveFileName(self, 'Saving As', "Document", "All Files (*)")
        self.__pressedSaved = True
        self.ui.plainTextEdit.blockSignals(False)
        if len(file[0]) > 0:
            # ensure that user gave a name to the file during saving
            FileManager.FileManager.append(self, file[0], self.ui.plainTextEdit.toPlainText())
            self.setWindowTitle(FileManager.FileManager.extractFileName(self, file[0]))
            self.__file_changed = False
            self.__saved = True
        else:
            self.__saved = False
            self.__file_changed = True
            self.__current_file = file[0]

    def closeEvent(self, event):
        # overwritten method to trigger an event when user closes the program
        # calls a dialog asking if user wants to save or discard the changes

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

    def pressEditUndo(self):

        self.ui.plainTextEdit.undo()

    def pressEditRedo(self):

        self.ui.plainTextEdit.redo()