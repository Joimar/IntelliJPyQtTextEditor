import os
from urllib.parse import urlparse
from PyQt6.QtWidgets import QFileDialog, QMessageBox


class FileManager:
    __file = ""

    @staticmethod
    def checkFile(str):

        if os.path.isfile(str):
            return True
        else:
            return False

    @staticmethod
    def extractFileName(name):

        return os.path.basename(urlparse(name).path)

    @staticmethod
    def updatingFile(file_path, content):
        """Overwrite the content of an existing file."""
        try:
            with open(file_path, "w") as f:
                # f.truncate(0)
                f.write(content)
                # f.close()

        except FileExistsError as error:
            print(f"Error when trying to update file: {error}.")

    @staticmethod
    def read(file_path):
        """Read the content of a file and returns it as string. In case of error, returns None"""
        try:
            with open(file_path, "r") as f:
                # f = open(file_path, "r")
                # content = f.read()
                # f.close()
                return f.read()
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return None
        except FileExistsError as error:
            print(f"Error: file does not exist: {error}.")
            return None
        except Exception as error:
            print(f"Error: Not possible to read the file: {error}")
            return None

    @staticmethod
    def append(name, content):
        f = open(name, "w")
        f.write(content)
        f.close()
