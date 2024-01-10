import os
from urllib.parse import urlparse
from PyQt6.QtWidgets import QFileDialog, QMessageBox


class FileManager:
    __file = ""

    def checkFile(self, str):

        if os.path.isfile(str):
            return True
        else:
            return False

    def extractFileName(self, name):

        return os.path.basename(urlparse(name).path)

    def updatingFile(self, name, content):

        try:
            f = open(name, "r+")
            f.truncate(0)
            f.write(content)
            f.close()

        except FileExistsError as error:
            print(error)

    def read(self, name):

        try:
            f = open(name, "r")
            content = f.read()
            f.close()
            return content
        except FileExistsError as error:
            print(error)
