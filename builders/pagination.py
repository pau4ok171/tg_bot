from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import config
import json
import math
from handlers.states import States

VERSION = config.version
TRANS_ID = [21, 50, 51, 53]
MAX_PAGE_BUTTONS_ON_LIST = 42
NAV_BUTTON_LIST_1 = ['first1', 'prev1', 'choice1', 'next1', 'last1']
NAV_BUTTON_LIST_2 = ['first2', 'prev2', 'choice2', 'next2', 'last2']


class TelegramPagination:
    def __init__(self, bt, db, cm, cl_2, bot_cm, pagin_id=0):
        self.bt = bt
        self.db = db
        self.cm = cm
        self.cl_2 = cl_2
        self.bot_cm = bot_cm

        self.handler = 'pagin'
        self.date = datetime.strftime(datetime.now().date(), '%d%m%Y')
        self.pagin_id = pagin_id
        self.session_id = VERSION

        self.prev_button = '<<'
        self.next_button = '>>'
        self.first_button = '<<<'
        self.last_button = '>>>'
        self. empty_nav_button = '×'
        self.empty_id_page_button = ' '

    def build_reply_markup(self, level, page=1, params=None) -> InlineKeyboardMarkup:
        buttons = None
        row_size = None
        last_page = None

        # Построить меню для книг
        if level == 1:
            # Создать лист книг-кнопок
            buttons = self._build_book_menu(page=page)
            last_page = math.ceil(int(self.cm.select_books_nb_non_read()) / 10)
            # Задать параметры
            row_size = 1

        # Построить меню для меню выбора страницы
        elif level == 2:
            buttons = self._build_page_menu(page=page, params=params)
            last_page = params['data']['l_p']
            # Задать параметры
            row_size = 7

        # Создать навигационные кнопки
        nav_buttons = self._build_navigation_buttons(
            page=page,
            last_page=last_page,
            level=level
        )

        # Создать нижние кнопки
        footer_buttons = self._build_footer_buttons()

        # Создать клавиатуру
        reply_markup = InlineKeyboardMarkup(
            self._build_menu(
                buttons,
                nav_buttons=nav_buttons,
                footer_buttons=footer_buttons,
                row_size=row_size
            )
        )

        return reply_markup

    def _build_book_menu(self, page):
        # Вернуть из бд набор из книг
        skip_page = (page - 1) * 10

        books = self.cm.select_books_for_pagination((skip_page,))
        books = [dict(zip(['id', 'author', 'name'], book)) for book in books]

        # Создать кнопки для книг
        buttons = []
        for book in books:
            name = 'object1'
            data = {'book_id': book['id']}

            text = f'id: {book["id"]} author: {book["author"]} name: {book["name"]}'
            callback_data = '&'.join((self.handler, name, self.session_id, str(data)))

            button = InlineKeyboardButton(text=text, callback_data=callback_data)
            buttons.append(button)

        return buttons

    def _build_page_menu(self, page, params) -> list[InlineKeyboardButton]:
        first = 1 + (MAX_PAGE_BUTTONS_ON_LIST * (page-1))
        last = MAX_PAGE_BUTTONS_ON_LIST * page
        last_page = params['data']['l_p']

        # Собрать кнопки страниц
        buttons = []
        for i in range(first, last+1):
            if i <= last_page:
                text = i
                name = 'object2'
            else:
                text = self.empty_id_page_button
                name = 'empty'

            data = {'c_p': i, 'l_p': last_page}
            callback_data = '&'.join((self.handler, name, self.session_id, str(data)))
            button = InlineKeyboardButton(text=text, callback_data=callback_data)
            buttons.append(button)

        return buttons

    def _build_navigation_buttons(self, page, last_page, level):

        navigations = self._build_nav_dict(
            page=page,
            last_page=last_page,
            level=level
        )

        # Создать навигационные кнопки
        nav_buttons = []
        for key, val in navigations.items():
            button = InlineKeyboardButton(text=val, callback_data=f'{key}')
            nav_buttons.append(button)

        return nav_buttons

    def _build_nav_dict(self, page, last_page, level) -> dict:
        max_page_nb = math.ceil(last_page / MAX_PAGE_BUTTONS_ON_LIST)  # Кол-во страниц кнопок страниц
        nav_button_list = NAV_BUTTON_LIST_1 if level == 1 else NAV_BUTTON_LIST_2
        nav_button = dict(zip(nav_button_list, nav_button_list))
        l_page = last_page if level == 1 else max_page_nb
        nav_b_name = {
            'first': self.first_button,
            'prev': self.prev_button,
            'choice': page,
            'next': self.next_button,
            'last': self.last_button}

        if page == 1:
            nav_button[f'first{level}'] = 'empty_f'
            nav_button[f'prev{level}'] = 'empty_p'
            nav_b_name['first'] = self.empty_nav_button
            nav_b_name['prev'] = self.empty_nav_button

        if page == l_page:
            nav_button[f'next{level}'] = 'empty_n'
            nav_button[f'last{level}'] = 'empty_l'
            nav_b_name['next'] = self.empty_nav_button
            nav_b_name['last'] = self.empty_nav_button

        nav_button_list = nav_button.values()

        data = {'c_p': page, 'l_p': last_page, 'max_p': max_page_nb}
        text = nav_b_name.values()
        callback_data = ['&'.join((self.handler, name, str(self.session_id), str(data))) for name in nav_button_list]

        navigations = dict(zip(callback_data, text))

        return navigations

    def _build_footer_buttons(self):
        # Создать лист нижних кнопок
        footer_buttons_id = [10024, 10026]
        footers = self.bt.get_buttons_by_id(footer_buttons_id, lang=self.bt.lang)

        # Создать нижние кнопки
        footer_buttons = []
        for key, val in footers.items():
            button = InlineKeyboardButton(text=val, callback_data=key)
            footer_buttons.append(button)

        return footer_buttons

    @staticmethod
    def _extract_call_data(call) -> dict:
        params = call.data.split('&')

        params = dict(
            zip(['handler', 'name', 'id', 'data'][:len(params)], params))

        params['data'] = params['data'].replace("\'", "\"") if params['data'] else '{}'

        params = {
            'handler': params['handler'],
            'name': params['name'],
            'id': params['id'],
            'data': json.loads(params['data']) or None,
        }

        return params

    @staticmethod
    def func():
        def validation(call):
            start = f'pagin&'
            return call.data.startswith(start)
        return validation

    async def process(self, bot, call):
        params = self._extract_call_data(call)

        action = params['name']

        # Обработка навигационных кнопок 1 уровня
        if action in NAV_BUTTON_LIST_1:
            await self._process_nav_call(level=1, bot=bot, call=call, params=params)

        # Обработка навигационных кнопок 2 уровня
        elif action in NAV_BUTTON_LIST_2:
            await self._process_nav_call(level=2, bot=bot, call=call, params=params)

        # Обработка объектов-кнопок 1 уровня
        elif action == 'object1':
            await self._process_book_call(bot, call, params)

        elif action == 'object2':
            await self._process_nav_call(level=1, bot=bot, call=call, params=params)

        else:
            return None

    async def _process_nav_call(self, level, bot, call, params):
        trans = self.cm.select_translation_by_id(TRANS_ID, self.bt.lang)
        action = params['name']
        current_page = params['data']['c_p']
        last_page = params['data']['l_p']
        max_page_nb = math.ceil(last_page / MAX_PAGE_BUTTONS_ON_LIST)  # Кол-во страниц кнопок страниц
        l_page = last_page if level == 1 else max_page_nb

        if action.startswith('first'):
            current_page = 1

        elif action.startswith('prev'):
            current_page -= 1

        elif action.startswith('next'):
            current_page += 1

        elif action.startswith('last'):
            current_page = l_page

        elif action.startswith('choice1'):
            current_page = 1
            level=2

        elif action.startswith('choice2'):
            current_page = 1
            level = 1

        elif action.startswith('object2'):
            current_page = current_page

        else:
            return None

        reply_markup = self.build_reply_markup(level=level, page=current_page, params=params)

        text = f'{trans[50]} {current_page} {trans[51]} {last_page if level == 1 else max_page_nb}'
        await self.bt.get_edited_text(bot, call, text, reply_markup)

    async def _process_book_call(self, bot, call, params):
        self.bt.lang = call.from_user.language_code
        trans = self.cm.select_translation_by_id(TRANS_ID, self.bt.lang)
        # Сохранить id книг в память
        book_id = params['data']['book_id']

        # Отчистить сохраненные состояния в памяти
        await bot.delete_state(call.message.from_user.id, call.message.id)

        # Открыть состояние id книги
        await bot.set_state(call.message.from_user.id,
                            States.book_id,
                            call.message.chat.id)

        # Сохранить состояние id книги в память
        async with bot.retrieve_data(call.message.from_user.id, call.message.chat.id) as data:
            data['book_id'] = book_id

        self.cl_2.locale = call.from_user.language_code
        # Добавить дополнительные кнопки в календарь
        self.cl_2.additional_buttons = self.bt.additional_buttons_for_get_read('started')
        # Построить календарь
        reply_markup, step = self.cl_2.build()

        # Отправить календарь пользователю
        text = f'{trans[53]}'
        await self.bot_cm.edit_message(call, text, reply_markup)

    @staticmethod
    def _build_menu(buttons, row_size, nav_buttons=None, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + row_size] for i in range(0, len(buttons), row_size)]

        if header_buttons:
            menu.insert(0, header_buttons)

        if nav_buttons:
            menu.append(nav_buttons)

        if footer_buttons:
            menu.append(footer_buttons)

        return menu