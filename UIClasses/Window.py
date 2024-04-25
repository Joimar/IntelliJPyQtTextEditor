# This Python file uses the following encoding: utf-8
import PyQt6
from PyQt6 import QtCore
from PySide6.QtCore import QFileInfo
#from PyQt6.QtPrintSupport import QPrinter, QPrintPreviewDialog, QPrintDialog
from PySide6.QtPrintSupport import QPrinter, QPrintPreviewDialog, QPrintDialog
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QFileDialog

from pdfrw import PdfWriter

import os.path

from UIClasses.FontSizeWindow import Ui_FontSize, FontSizeWindow
from UIFiles.UIMainWindow import Ui_MainWindow
from Managers import FileManager


class MainWindow(QMainWindow):
    __current_file = ""
    __file_changed = False
    __saved = False
    __pressedSaved = False
    __fontSizeWindow = None

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
        self.ui.actionPrint.triggered.connect(self.pressFilePrint)
        self.ui.actionExport_PDF.triggered.connect(self.pressExportPDF)
        # Edit Actions
        self.ui.actionUndo.triggered.connect(self.pressEditUndo)
        self.ui.actionRedo.triggered.connect(self.pressEditRedo)

        # Appearance Actions
        self.ui.actionSet_Dark_Mode.triggered.connect(self.pressAppearanceSetDarkMode)
        self.ui.actionSet_Light_Mode.triggered.connect(self.pressAppearanceSetLightMode)
        self.ui.actionChange_Font_Size.triggered.connect(self.pressAppearanceChangeFont)

        self.ui.plainTextEdit.textChanged.connect(self.__setFileChanged)

        self.setWindowTitle("Text Editor")

        # actions from font size window


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
            # if not exist yet
            file = QFileDialog.getSaveFileName(self, 'Saving File', "Document", 'Text files (*.txt)')
            self.__pressedSaved = True
            self.ui.plainTextEdit.blockSignals(False)
            if len(file[0]) > 0:
                FileManager.FileManager.append(self, file[0], self.ui.plainTextEdit.toPlainText())
                self.setWindowTitle(FileManager.FileManager.extractFileName(self, file[0]))
                self.__file_changed = False
                self.__saved = True
            else:
                self.__saved = False
                self.__file_changed = True
            self.__current_file = file[0]

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
    def pressFilePrint(self):

        printer = QPrinter()
        previewDialog = QPrintPreviewDialog(printer)
        previewDialog.paintRequested.connect(self.ui.plainTextEdit.print_)
        previewDialog.exec_()

        #if dialog.exec_() == QPrintDialog.accepted:
        #    self.ui.plainTextEdit.print_(printer)

    def pressExportPDF(self):
        # test = PdfWriter()
        # test.addpage(self.ui.plainTextEdit)
        # test.write("test.pdf")
        fn, _ = QFileDialog.getSaveFileName(self, "Export PDF", None, "PDF files (.pdf);;All Files")

        if fn != '':
            if QFileInfo(fn).suffix() == "":
                fn += '.pdf'
                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                printer.setOutputFileName(fn)
                self.ui.plainTextEdit.document().print_(printer)

    def pressAppearanceSetDarkMode(self):

        self.setStyleSheet('''QWidget{
            background-color: rgb(33,33,33);
            color: #FFFFFF;
            }
            QPlainTextEdit{
            background-color: rgb(46,46,46);
            }
            QMenuBar::item:selected{
            color: #000000
            } ''')

    def pressAppearanceSetLightMode(self):

        self.setStyleSheet("")
        self.ui.plainTextEdit.font().setPointSize(90)


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
        # TODO create a conditional to use close() only when fontSizeWindow is not None
        if self.__fontSizeWindow is not None:
            self.__fontSizeWindow.close()

    def pressEditUndo(self):

        self.ui.plainTextEdit.undo()

    def pressEditRedo(self):

        self.ui.plainTextEdit.redo()

    def pressAppearanceChangeFont(self):

        self.__fontSizeWindow = FontSizeWindow(self.ui.plainTextEdit)
        self.__fontSizeWindow.__fontSize = self.ui.plainTextEdit.fontInfo().pointSize()

        self.__fontSizeWindow.ui.spinBox.setValue(self.ui.plainTextEdit.fontInfo().pointSize())
        self.__fontSizeWindow.ui.spinBox.valueChanged.connect(self.updateFontSize)

        self.__fontSizeWindow.show()

    def updateFontSize(self):

        self.ui.plainTextEdit.setFont(QFont('Arial', self.__fontSizeWindow.ui.spinBox.value()))



