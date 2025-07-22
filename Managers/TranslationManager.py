import gettext
import os
from pathlib import Path


class TranslationManager:
    def __init__(self):
        self.locale_dir = Path(__file__).parent / "locales"
        self.current_language = 'en'
        self.translation = gettext.NullTranslations()

    def set_language(self, lang: str):
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
