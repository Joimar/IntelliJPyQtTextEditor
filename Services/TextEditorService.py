import os

from Managers.FileManager import FileManager


class TextEditorService:
    def __init__(self):
        # self._current_text = ""
        # self._file_name = ""

        self._file_path = ""
        self._is_modified = False

        self._saved = False
        self._is_updating = False

    def on_text_changed(self):
        if self._is_updating:
            return

        if self._saved:
            self._is_modified = False
            self._is_updating = False
        else:
            self._is_modified = True
            self._is_updating = True
        self._saved = False
    def new_file(self):
        # self._current_text = ""
        self._file_path = ""
        self._is_modified = False

    def open_file(self, file_path):
        if file_path:
            self._file_path = file_path
            self._is_modified = False
            self._is_updating = False
            self._saved = True

            return FileManager.read(file_path)

        return None

    def save_file(self, text):
        self._saved = True
        FileManager.updatingFile(self._file_path, text)
        self._is_modified = False
        self._is_updating = False

    def save_as(self, text, file_path):
        if file_path:
            FileManager.append(file_path, text)
            self._is_modified = False
            self._saved = True
            self._file_path = file_path
            self._is_updating = False
        else:
            self._saved = False
            self._is_modified = True
            self._is_updating = True

    def file_exist(self):
        return FileManager.checkFile(self._file_path)

    def set_text(self, text):
        # self._current_text = text
        self._is_modified = True

    def get_file_path(self):
        return self._file_path

    def set_file_path(self, file_path):
        self._file_path = file_path

    def get_file_name(self):
        return "Untitled" if not self._file_path else os.path.basename(self._file_path)

    def set_is_modified(self, is_modified):
        self._is_modified = is_modified

    def get_modified(self):
        return self._is_modified

    def set_save(self, save):
        self._saved = save

    def get_saved(self):
        return self._saved

    def set_is_updating(self, is_updating):
        self._is_updating = is_updating

    def get_is_updating(self):
        return self._is_updating
