import schemas


class Keyboard:
    def __init__(self, bot=None, bt=None, db=None, cm=None, bot_cm=None):
        self.bot = bot
        self.bt = bt
        self.db = db
        self.cm = cm
        self.bot_cm = bot_cm
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
            self.trans = self.cm.select_translations(self.lang)
