# This Python file uses the following encoding: utf-8
import os
from Utils.AppStrings import AppStrings
from PySide6.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QFileDialog
from PySide6.QtCore import QCoreApplication, QTranslator
from PySide6.QtCore import Slot
from Services.SpellCheckingHighLighter import SpellCheckingHighLighter
from StyleFiles.AppThemes import AppTheme

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

        self.highlighter = SpellCheckingHighLighter(self.ui.plainTextEdit.document())
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

        # Language Actions
        self.ui.actionpt.triggered.connect(lambda: self.set_language('pt_BR'))
        self.ui.actionen.triggered.connect(lambda: self.set_language('en'))
        self.ui.actiones.triggered.connect(lambda: self.set_language('es'))
        self.ui.actionfr.triggered.connect(lambda: self.set_language('fr'))
        self.ui.actionde.triggered.connect(lambda: self.set_language('de'))
        self.ui.actionru.triggered.connect(lambda: self.set_language('ru'))

        # Spell Checker settings

        #self.ui.plainTextEdit.textChanged.connect(self.__on_text_changed)

        self.ui.plainTextEdit.document().modificationChanged.connect(self.__on_text_changed)

        # Messages for external windows
        self.Export_pdf = AppStrings.EXPORT_PDF

        self.setWindowTitle("Text Editor")
        self.set_language('en')
        # actions from font size window
        # d = enchant.Dict("en_US")

    @Slot(bool)
    def __on_text_changed(self, changed):

        self.__service.on_text_changed(changed)

        self.updateWindowTitle()


    def press_file_new(self):
        # creates new file and cleans plaintext
        self.__service.new_file()
        self.ui.plainTextEdit.clear()
        self.updateWindowTitle()

    # Open Functionalities are done
    def pressFileOpen(self):
        # Opens a specific txt file selected by user
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   QCoreApplication.translate(*AppStrings.OPEN_FILE), '', 'Text '
                                                                                                          'files '
                                                                                                          '(*.txt)')

        text = self.__service.open_file(file_path)
        if text is not None:
            self.ui.plainTextEdit.setPlainText(text)
            self.updateWindowTitle()

    def pressFileSave(self):
        text = self.ui.plainTextEdit.toPlainText()
        if self.__service.file_exist():
            self.__service.save_file(text)
            self.ui.plainTextEdit.document().setModified(False)
        else:
            self.pressFileSaveAs()

    def pressFileSaveAs(self):
        # save a file or modification when user clicks in save option
        text = self.ui.plainTextEdit.toPlainText()
        file_path, _ = QFileDialog.getSaveFileName(self, QCoreApplication.translate(*AppStrings.SAVING_FILE),
                                                   "Document", 'Text files (*.txt)')

        if self.__service.save_as(text, file_path):
            self.ui.plainTextEdit.document().setModified(False)

        # print("Modificado? " + self.ui.plainTextEdit.document().isModified().__str__())

        self.updateWindowTitle()

    def pressFilePrint(self):

        printer = QPrinter()
        previewDialog = QPrintPreviewDialog(printer)
        previewDialog.paintRequested.connect(self.ui.plainTextEdit.print_)
        previewDialog.exec_()

    def pressExportPDF(self):
        """Exports the current document as a PDF file."""

        file_path, _ = QFileDialog.getSaveFileName(self, QCoreApplication.translate(*self.Export_pdf), "",
                                                   "PDF files (*.pdf);;All Files")

        if not file_path:  # Verify if user canceled the dialog
            return

        # Ensure that the extensions .pdf be correctly added
        if not file_path.lower().endswith(".pdf"):
            file_path += ".pdf"

        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFileName(file_path)
            self.ui.plainTextEdit.document().print_(printer)

            message_file_path = QCoreApplication.translate(*AppStrings.SAVING_FILE).format(file_path)
            message_exported_pdf = QCoreApplication.translate(*AppStrings.EXPORT_COMPLETED)

            QMessageBox.information(self, message_exported_pdf, message_file_path)  # Message of success

        except Exception as e:  # Captura possíveis erros
            QMessageBox.critical(self, QCoreApplication.translate(*AppStrings.EXPORT_ERROR),
                                 f"{QCoreApplication.translate(*AppStrings.EXPORT_ERROR_MESSAGE)}{str(e)}")

    def pressAppearanceSetDarkMode(self):

        self.apply_stylesheet(AppTheme.DARK)

    def pressAppearanceSetLightMode(self):

        self.apply_stylesheet(AppTheme.LIGHT)

    def apply_stylesheet(self, theme: AppTheme):
        """Apply a specific style to the application."""
        self.setStyleSheet(theme.value)

    def closeEvent(self, event):
        # overwritten method to trigger an event when user closes the program
        # calls a dialog asking if user wants to save or discard the changes

        if self.__service.get_modified():
            box = QMessageBox()
            box.setWindowTitle(AppStrings.PROGRAM_NAME[1])
            box.setText(QCoreApplication.translate(*AppStrings.SAVE_CHANGES_QUESTION))
            box.setStandardButtons(
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

            returnValue = box.exec()
            if returnValue == QMessageBox.StandardButton.Save:

                self.ui.plainTextEdit.document().setModified(False)
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

            if self.ui.plainTextEdit.document().isModified():

                self.setWindowTitle(file_name + "*")
            else: self.setWindowTitle(file_name)


    def set_language(self, lang):

        app = QApplication.instance()
        # Remove tradutor antigo
        if hasattr(self, "_translator") and self._translator:
            app.removeTranslator(self._translator)

        if hasattr(self, "_qt_translator") and self._qt_translator:
            app.removeTranslator(self._qt_translator)

        # Carrega novo tradutor

        translation_file = f"Translations/{lang}.qm"
        self._translator = QTranslator()

        translation_native_file = f"Translations/qtbase_{lang}.qm"
        self._qt_base_translator = QTranslator()

        if os.path.exists(translation_file) and self._translator.load(translation_file):
            app.installTranslator(self._translator)
            print(f"Idioma alterado para: {lang}")

            # Força a retradução de toda a UI
            # self.ui.retranslateUi(self)
            # Retraduz strings manuais
            # self.retranslateUi()

        if os.path.exists(translation_native_file) and self._qt_base_translator.load(translation_native_file):
            app.installTranslator(self._qt_base_translator)
            print(f"Idioma alterado para o padrão: qtbase_{lang}")

        self.ui.retranslateUi(self)
        self.retranslateUi()

        if lang == "pt_BR":
            self.highlighter.set_language("pt")
        else:
            self.highlighter.set_language(lang)

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Text Editor"))

        self.Export_pdf = AppStrings.EXPORT_PDF

        self.ui.menuFile.setTitle(QCoreApplication.translate(*AppStrings.MENU_FILE))
        self.ui.actionNew.setText(QCoreApplication.translate(*AppStrings.ACTION_NEW))
        self.ui.actionOpen.setText(QCoreApplication.translate(*AppStrings.ACTION_OPEN))
        self.ui.actionSave.setText(QCoreApplication.translate(*AppStrings.ACTION_SAVE))
        self.ui.actionSave_as.setText(QCoreApplication.translate(*AppStrings.ACTION_SAVE_AS))
        self.ui.actionPrint.setText(QCoreApplication.translate(*AppStrings.ACTION_PRINT))
        self.ui.actionExport_PDF.setText(QCoreApplication.translate(*AppStrings.ACTION_EXPORT_PDF))

        self.ui.menuEdit.setTitle(QCoreApplication.translate(*AppStrings.MENU_EDIT))
        self.ui.actionRedo.setText(QCoreApplication.translate(*AppStrings.ACTION_REDO))
        self.ui.actionUndo.setText(QCoreApplication.translate(*AppStrings.ACTION_UNDO))

        self.ui.menuAppearance.setTitle(QCoreApplication.translate(*AppStrings.MENU_APPEARANCE))
        self.ui.actionSet_Dark_Mode.setText(QCoreApplication.translate(*AppStrings.ACTION_SET_DARK_MODE))
        self.ui.actionSet_Light_Mode.setText(QCoreApplication.translate(*AppStrings.ACTION_SET_LIGHT_MODE))
        self.ui.actionChange_Font_Size.setText(QCoreApplication.translate(*AppStrings.ACTION_CHANGE_FONT_SIZE))

