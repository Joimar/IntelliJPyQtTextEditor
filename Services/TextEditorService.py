import os

from Managers.FileManager import FileManager


class TextEditorService:
    def __init__(self):
        # self._current_text = ""

        self._file_path = ""
        self._is_modified = False
        self.__text = ""

    def on_text_changed(self, changed):
        self._is_modified = changed

    def new_file(self):
        # self._current_text = ""
        self._file_path = ""
        self._is_modified = False

    def open_file(self, file_path):
        if file_path:
            self._file_path = file_path
            return FileManager.read(file_path)

        return None

    def save_file(self, text):
        if self.file_exist():
            FileManager.updatingFile(self._file_path, text)
            self.set_text(text)
            return True

        return False

    def save_as(self, text, file_path):
        if file_path:
            FileManager.append(file_path, text)
            self.set_text(text)
            self._file_path = file_path
            return True
        else:
            return False

    def file_exist(self):
        return FileManager.checkFile(self._file_path)

    def set_text(self, text):
        self.__text = text
        self._is_modified = True

    def get_file_path(self):
        return self._file_path

    def set_file_path(self, file_path):
        self._file_path = file_path

    def get_file_name(self):
        return "Untitled" if not self._file_path else os.path.basename(self._file_path)

    def get_modified(self):
        return self._is_modified
