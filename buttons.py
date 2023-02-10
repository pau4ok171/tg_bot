from telebot import types
from command import CommandManager
import config
from datetime import datetime
from database import DatabaseManager
import json
import random
import private_access

ADMINS = config.admins
VERSION = config.version
TRANS_ID = [1, 2]
BUTTONS = {
    'header': [],
    'header_admin': [],
    'main': [],
    'main_admin': [],
    'footer': [],
    'footer_admin': [],
}

cm = CommandManager()
db = DatabaseManager()

class ButtonsManager:
    def __init__(self, bot_cm):
        self.lang = 'ru'
        self.trans = cm.select_translation_by_id(TRANS_ID, self.lang)
        self.row_size = 2
        self.menu_el_size = 1
        self.bot_cm = bot_cm

    def additional_buttons_for_get_read(self, action) -> list[list[dict]]:
        trans = cm.select_translation_by_id(TRANS_ID, self.lang)

        additional_buttons = [
                    [{'text': f'{trans[1]}', 'callback_data': f'calender_{action}_cancel'},
                     {'text': f'{trans[2]}', 'callback_data': 'calender_home'}]
        ]

        return additional_buttons

    def build_get_books_read(self, message):
        main_buttons = dict(cm.select_reading_books())

        buttons = {
            'main': self.form_buttons_for_books(main_buttons),
            'footer': [10024, 10026],
        }

        reply_markup = self._build_menu(buttons, message, size=self.menu_el_size)

        return reply_markup

    def build_start_menu(self, message):

        buttons = {
            'header_admin': [10008],
            'main': [10004, 10005, 10006, 10007, 10022],
            'main_admin': [10023]
        }

        reply_markup = self._build_menu(buttons, message)

        return reply_markup

    def build_common_stats(self, message):

        buttons = {
            'main': [10010, 10011],
            'footer': [10003]
        }

        reply_markup = self._build_menu(buttons, message)

        return reply_markup

    def build_stats_by_category(self, message):

        buttons = {
            'main': [10012, 10013, 10014],
            'footer': [10003]
        }

        reply_markup = self._build_menu(buttons, message)

        return reply_markup

    def build_stats_by_language(self, message):

        buttons = {
            'main': [10015, 10016],
            'footer': [10003]
        }

        reply_markup = self._build_menu(buttons, message)

        return reply_markup

    def build_stats_by_category_and_lang(self, message):

        buttons = {
            'main': [10017],
            'footer': [10003]
        }

        reply_markup = self._build_menu(buttons, message)

        return reply_markup

    # Управление книгами
    def build_for_books_management(self, message):

        buttons = {
            'main': [10009, 10025],
            'footer': [10003]
        }

        reply_markup = self._build_menu(buttons, message)

        return reply_markup

    # TOP BOOKS
    def build_to_read(self, message):

        buttons = {
            'main': [10018],
            'footer': [10003]
        }

        reply_markup = self._build_menu(buttons, message)

        return reply_markup

    def build_admin_panel(self, message):

        buttons = {
            'main': [10019],
            'footer': [10003]
        }

        reply_markup = self._build_menu(buttons, message)

        return reply_markup

    def build_confirm_adding(self, action, message):

        buttons = {
            'main': [10020, 10021] if action == 'finished' else [10028, 10029],
        }

        reply_markup = self._build_menu(buttons, message)

        return reply_markup

    def _build_menu(self, buttons, message, size=None) -> types.InlineKeyboardMarkup:
        size = size or self.row_size
        buttons =  BUTTONS | buttons
        admin_buttons = {k.replace('_admin', ''): v for k, v in buttons.items() if k.endswith('admin')}
        buttons = {k: v for k, v in buttons.items() if not k.endswith('admin')}

        is_admin = private_access.is_admin(message)

        if is_admin:
            buttons = {k: v + admin_buttons[k] for k, v in buttons.items()}

        buttons = [self._build_buttons(buttons) for buttons in buttons.values()]

        menu = [buttons[1][i:i + size] for i in range(0, len(buttons[1]), size)]
        if buttons[0]: menu.insert(0, buttons[0])
        if buttons[2]: menu.append(buttons[2])

        reply_markup = types.InlineKeyboardMarkup(menu)

        return reply_markup

    def _build_buttons(self, buttons: list) -> list[list]:
        buttons: dict = self.get_buttons_by_id(buttons, lang=self.lang) or {}

        buttons: list = [types.InlineKeyboardButton(v, callback_data=k) for k, v in buttons.items()]

        return buttons

    def _build_callback_data(self):
        pass

    @staticmethod
    def process_callback_data(call) -> dict:
        """
        Формирует из ключа кнопки словарь с переменными для дальнейшей обработки
        :param call: 'client&books_nb&1.0.0&24052010&45898&{"book_id": 123, "book_name": "PRAVDA"}'
        :return: dict{}
        """
        params = call.data.split('&')

        params = dict(
            zip(['handler', 'name', 'version', 'date', 'id', 'data'][:len(params)], params))

        params['data'] = params['data'].replace("\'", "\"")
        params = {
            'handler': params['handler'],
            'name': params['name'],
            'version': params['version'],
            'date': datetime.strptime(params['date'], '%d%m%Y').date(),
            'id': int(params['id']),
            'data': json.loads(params['data']) or None,
        }

        return params

    @staticmethod
    def get_buttons_by_id(buttons_id: list, lang: str, data: dict=None) -> dict | None:
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
    def form_buttons_for_books(response: dict):

        handler = 'admin'
        name = 'get_read'
        date = datetime.strftime(datetime.now().date(), '%d%m%Y')

        button_callback = []
        text = []

        for key, val in response.items():
            button_id = random.randint(1, int(1e18))
            trans = val
            data = {'id': key}
            button_callback.append(
                '&'.join([handler, name, VERSION, str(date), str(button_id), str(data)]))
            text.append(trans)

        # Сформировать словарь из callback и text
        buttons = dict(
            zip(button_callback, text))

        return buttons

