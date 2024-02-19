from PySide6.QtWidgets import QMainWindow

from UIFiles.UIFontSize import Ui_FontSize


class FontSizeWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_FontSize()
        self.ui.setupUi(self)
