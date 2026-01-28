import gettext
import os
from pathlib import Path

from PySide6.QtWidgets import QApplication

from UIClasses.Window import MainWindow


# Turno this class into Facade
class TranslationManager:
    def __init__(self):
        self.locale_dir = Path(__file__).parent / "locales"
        self.current_language = 'en'
        self.translation = gettext.NullTranslations()

        self._translator_customized = None
        self._translator_qt = None

    def set_language(self, lang: str):

        app = QApplication.instance()
        # Remove tradutor antigo
        if hasattr(self, "_translator_customized") and self._translator_customized:
            app.removeTranslator(self._translator_customized)

        if hasattr(self, "_translator_qt") and self._translator_qt:
            app.removeTranslator(self._translator_qt)

        self.current_language = lang
        try:
            self.translation = gettext.translation(
                'messages',
                localedir=self.locale_dir,
                languages=[lang]
            )
        except FileNotFoundError:
            self.translation = gettext.NullTranslations()  # Fallback para inglês

    def gettext(self, text):
        return self.translation.gettext(text)



# Instância global
translator = TranslationManager()
_ = translator.gettext
