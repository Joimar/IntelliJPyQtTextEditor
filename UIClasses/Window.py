# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QFileInfo
from PySide6.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QFileDialog
from StyleFiles.AppThemes import AppTheme
import enchant

from UIClasses.FontSizeWindow import FontSizeWindow
from UIFiles.UIMainWindow import Ui_MainWindow

from Services.TextEditorService import TextEditorService


class MainWindow(QMainWindow):

    __fontSizeWindow = None
    # Criando instância do serviço antes de usá-lo
    __service = TextEditorService()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__is_updating = False

        # File Actions
        self.ui.actionNew.triggered.connect(self.press_file_new)
        self.ui.actionSave.triggered.connect(self.pressFileSave)
        self.ui.actionSave.triggered.connect(self.ui.plainTextEdit.textChanged)
        self.ui.actionSave_as.triggered.connect(self.pressFileSaveAs)
        self.ui.actionSave_as.triggered.connect(self.ui.plainTextEdit.textChanged)
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

        self.ui.plainTextEdit.textChanged.connect(self.__on_text_changed)

        self.setWindowTitle("Text Editor")

        # actions from font size window
        # d = enchant.Dict("en_US")

    def __on_text_changed(self):
        self.__service.on_text_changed()

    def press_file_new(self):
        # creates new file and cleans plaintext
        self.__service.new_file()
        self.ui.plainTextEdit.clear()
        self.updateWindowTitle()

    # Open Functionalities are done
    def pressFileOpen(self):
        # Opens a specific txt file selected by user
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'Text files (*.txt)')
        text = self.__service.open_file(file_path)
        if text is not None:
            self.ui.plainTextEdit.setPlainText(text)
            self.updateWindowTitle()

    def pressFileSave(self):
        text = self.ui.plainTextEdit.toPlainText()
        if self.__service.file_exist():
            self.__service.save_file(text)
        else:
            self.pressFileSaveAs()

    def pressFileSaveAs(self):
        # save a file or modification when user clicks in save option
        text = self.ui.plainTextEdit.toPlainText()
        file_path, _ = QFileDialog.getSaveFileName(self, 'Saving File', "Document", 'Text files (*.txt)')
        self.__service.save_as(text, file_path)
        self.updateWindowTitle()

    def pressFilePrint(self):

        printer = QPrinter()
        previewDialog = QPrintPreviewDialog(printer)
        previewDialog.paintRequested.connect(self.ui.plainTextEdit.print_)
        previewDialog.exec_()

    def pressExportPDF(self):
        """Exports the current document as a PDF file."""

        file_path, _ = QFileDialog.getSaveFileName(self, "Export PDF", "", "PDF files (*.pdf);;All Files")
        if not file_path:  # Verify if user canceled the dialog
            return

        # Ensure that the extensions .pdf be correctly added
        if not file_path.lower().endswith(".pdf"):
            file_path += ".pdf"

        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFileName(file_path)
            self.ui.plainTextEdit.document().print_(printer)
            QMessageBox.information(self, "Export Completed", f"File saved in:\n{file_path}")  # Message of success

        except Exception as e:  # Captura possíveis erros
            QMessageBox.critical(self, "Error of Exporting", f"Not possible to export PDF file.\nErro: {str(e)}")

    def pressAppearanceSetDarkMode(self):
        # Bug report: when in darkmode, items in menu bar chenge paddings

        # self.setStyleSheet('''QWidget{
        #     background-color: rgb(33,33,33);
        #     color: #FFFFFF;
        #     }
        #     QPlainTextEdit{
        #     background-color: rgb(46,46,46);
        #     }
        #     QMenuBar::item:selected{
        #     color: #000000
        #     } ''')

        self.apply_stylesheet(AppTheme.DARK)

    def pressAppearanceSetLightMode(self):

        self.setStyleSheet("")
        self.ui.plainTextEdit.font().setPointSize(90)

    def apply_stylesheet(self, theme: AppTheme):
        """Apply a specific style to the application."""
        self.setStyleSheet(theme.value)

    def closeEvent(self, event):
        # overwritten method to trigger an event when user closes the program
        # calls a dialog asking if user wants to save or discard the changes

        if self.__service.get_modified():
            box = QMessageBox()
            box.setWindowTitle("Program Name")
            box.setText("Do you want to save the changes?")
            box.setStandardButtons(
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

            returnValue = box.exec()
            if returnValue == QMessageBox.StandardButton.Save:
                self.__service.set_is_modified(False)
                self.__service.set_save(True)
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

    def updateWindowTitle(self):
        if self.__service.file_exist():
            file_name = self.__service.get_file_name()
            self.setWindowTitle(file_name)
