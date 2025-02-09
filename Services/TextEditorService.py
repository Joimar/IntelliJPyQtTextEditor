import os


class TextEditorService:
    def __init__(self):
        self._current_text = ""
        self._file_path = None
        self._is_modified = False

    def new_file(self):
        self._current_text = ""
        self._file_path = None
        self._is_modified = False

    def open_file(self, file_path):
        with open(file_path, "r") as file:
            self._current_text = file.read()
        self._file_path = file_path
        self._is_modified = False

    def save_file(self):
        if self._file_path:
            with open(self._file_path, "w") as file:
                file.write(self._current_text)
            self._is_modified = False
        else:
            raise ValueError("Nenhum arquivo especificado")

    def set_text(self, text):
        self._current_text = text
        self._is_modified = True

    def get_text(self):
        return self._current_text

    def get_file_name(self):
        return "Untitled" if not self._file_path else os.path.basename(self._file_path)