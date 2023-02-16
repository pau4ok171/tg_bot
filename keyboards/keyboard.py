import schemas
from command import CommandManager


cm = CommandManager()


class Keyboard:
    def __init__(self):
        self.lang = 'ru'
        self.trans = None

    @staticmethod
    def _build_keyboard(text, reply_markup):
        return schemas.Keyboard(text=text, reply_markup=reply_markup)

    def set_user_lang(self, response):
        """
        Изменить язык интерфейса если язык пользователя отличается.
        """
        lang = response.from_user.language_code

        if not self.trans or lang != self.lang:
            self.lang = lang
            self.trans = cm.select_translations(self.lang)
