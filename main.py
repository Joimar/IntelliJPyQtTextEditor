import sys

from PySide6.QtWidgets import QApplication
from UIClasses.Window import MainWindow


if __name__ == '__main__':
    #print("Hello World!!!")
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())