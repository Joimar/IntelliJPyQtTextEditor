from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCharFormat, QSyntaxHighlighter, QTextDocument
from spellchecker import SpellChecker
import re


class SpellCheckingHighLighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._language = 'pt'  # Idioma padrão
        self.spell = SpellChecker(language=self._language)
        self.error_format = QTextCharFormat()
        self.error_format.setUnderlineColor(Qt.red)
        self.error_format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

    def highlightBlock(self, text):

        words = text.split()
        for word in words:
            if not self.spell.known([word]):  # Verifica se a palavra é desconhecida
                # index = text.index(word)
                index = self.occurrences_indexes(text, word)
                for i in index:
                    self.setFormat(i, len(word), self.error_format)
        # words.clear()

    def set_language(self, lang):
        """Altera o idioma do verificador ortográfico e reaplica o realce"""
        self._language = lang
        self.spell = SpellChecker(language=self._language)
        self.rehighlight()  # Isso força a reavaliação de todo o texto

    def occurrences_indexes(self, text, word):
        indexes = []
        start_index = 0
        # Construct the regex pattern with word boundaries
        pattern = r"\b" + re.escape(word) + r"\b"

        for match in re.finditer(pattern, text):
            indexes.append(match.start())

        return indexes
