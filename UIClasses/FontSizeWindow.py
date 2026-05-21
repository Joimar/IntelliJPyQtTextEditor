from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QPlainTextEdit

from UIFiles.UIFontSize import Ui_FontSize


class FontSizeWindow(QMainWindow):
    __fontSize = None

    def __init__(self, plainText: QPlainTextEdit, parent=None):
        super().__init__(parent)

        self.ui = Ui_FontSize()
        self.ui.setupUi(self)

        self.ui.spinBox.valueChanged.connect(self.__updateTextSize(plainText))

    def __updateTextSize(self, plainText: QPlainTextEdit):
        plainText.setFont(QFont('Arial', self.ui.spinBox.value()))
        print("VRAU")
        print(self.ui.spinBox.value())
        # plainText.font().setPointSize(self.ui.spinBox.value())
