import schemas
from commands import CommandManager
from database import DatabaseManager
from datetime import datetime
import config
from telebot.types import InlineKeyboardButton


cm = CommandManager()
db = DatabaseManager()


VERSION = config.version


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

    @staticmethod
    def get_buttons_by_id(buttons_id: list, lang: str) -> dict | None:
        if not buttons_id:
            return None

        # Сформировать query
        query = cm.select_token_params(lang)

        # Получить данные из бд в нужном формате
        response = [db.crud_data(query, (str(button_id),), resp_type='rows')[0] for button_id in buttons_id]

        # Сформировать button_callback
        # и текстовую часть
        button_callback = []
        text = []
        for res in response:
            handler = res[0]
            name = res[1]
            button_id = res[2]
            trans = res[4] or res[3]
            date = datetime.strftime(datetime.now().date(), '%d%m%Y')
            data = {}

            button_callback.append(
                '&'.join([handler, name, VERSION, str(date), str(button_id), str(data)]))
            text.append(trans)

        # Сформировать словарь из callback и text
        buttons = dict(
            zip(button_callback, text))

        return buttons

    @staticmethod
    def _build_buttons(text: list, callback: list, size: int) -> list[list[InlineKeyboardButton]]:
        buttons = [[
            InlineKeyboardButton(
                text=v,
                callback_data=k
            ) for k, v in dict(zip(callback, text)).items()
        ]]

        buttons = [buttons[0][i:i + size] for i in range(0, len(buttons[0]), size)]

        return buttons
