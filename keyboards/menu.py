import config
from private_access import get_user_access_level

from keyboards.keyboard import Keyboard
from commands import CommandManager
from datetime import date


VERSION = config.version
AVAILABLE_LANGUAGUES = config.available_languagues


cm = CommandManager()


class MenuManager(Keyboard):
    def __init__(self, bt, calendars, paginations):
        # Инициализация родительского класса
        super().__init__()

        self.bt = bt
        self.calendars = calendars
        self.paginations = paginations

    """---------------------------------СТАРТ---------------------------------"""
    # Стартовое меню
    def build_start_menu_kb(self, response):
        text = f'{self.trans[24]}, <b>{response.from_user.first_name}!</b> {self.trans[25]}!\n{self.trans[26]}'
        reply_markup = self.bt.build_start_menu(response)
        return self._build_keyboard(text, reply_markup)

    """-----------------------------АДМИН__ПАНЕЛЬ-----------------------------"""
    # Меню управления книгами
    def build_book_management_kb(self, response):
        text = f'{self.trans[48]}'
        reply_markup = self.bt.build_books_management(response)
        return self._build_keyboard(text, reply_markup)

    # Панель администратора
    def build_admin_panel_kb(self, response):
        text = f'{self.trans[23]}'
        reply_markup = self.bt.build_admin_panel(response)
        return self._build_keyboard(text, reply_markup)

    # Уникальные пользователи
    def build_unique_users_kb(self, response):
        text = f'{self.trans[23]}'
        text += cm.select_admin_unique_users()
        reply_markup = self.bt.build_footer_buttons(menu_id='A1', response=response)
        return self._build_keyboard(text, reply_markup)

    """-------------------------------ПАГИНАЦИЯ-------------------------------"""
    # Пагинация в зависимости от pagin_id
    def build_pagin_kb(self, call, pagin_id):
        return self.paginations.build_pagin_kb(call, pagin_id)

    # Пагинация в зависимости от pagin_id
    def process_pagin_kb(self, pagin_id, call):
        return self.paginations.process_pagin_kb(pagin_id, call)

    """-------------------------------КАЛЕНДАРЬ-------------------------------"""
    # Календарь в зависимости от calendar_id
    async def build_calendar_kb(self, bot_cm, response, book_id, calendar_id):
        # Reset машины состояния
        await bot_cm.reset_state_data(response, calendar_id)
        # Сохранить состояние id книги в память
        await bot_cm.set_book_id(response, book_id, calendar_id)

        # Задать минимальную дату для календаря
        self.calendars.set_min_date(calendar_id, cm.select_started_by_id(book_id))

        # Построить календарь
        kb, chosen_date = self.calendars.build_calendar_kb(response, calendar_id)

        return kb

    def process_calendar_kb(self, call, calendar_id):
        return self.calendars.process_calendar(call, calendar_id)

    async def process_calendar_result(self, bot_cm, res, calendar_id, call):

        if calendar_id == 1:
            date_name = 44
            reply_markup = self.bt.build_confirm_adding(calendar_id, call)
        elif calendar_id == 2:
            date_name = 52
            reply_markup = self.bt.build_confirm_adding(calendar_id, call)
        else:
            return None

        # Записываем в машину состояния данные о дате
        values = await bot_cm.set_date(res, call, calendar_id)

        book_name = cm.select_book_name_by_id(values[1])
        act_date = date.strftime(values[0], '%d-%m-%Y')

        # Запросить у пользователя подтверждение для внесения изменения в бд
        text = f'<b>{self.trans[43]}:</b> {book_name}\n' \
               f'<b>{self.trans[date_name]}:</b> {act_date}\n' \
               f'<b>{self.trans[45]}</b>'

        return self._build_keyboard(text, reply_markup)

    def build_calendar_cancel_kb(self, response, pagin_id):
        return self.paginations.build_pagin_kb(response, pagin_id)

    """-----------------------------ИНФО_В_БД-----------------------------"""
    async def process_confirm_crud_book(self, bot_cm, call, calendar_id):
        values = await bot_cm.get_data(call, calendar_id)

        # Отправить команду на добавление данных в бд
        if calendar_id == 1:
            cm.get_read(values)
            menu_id='O1'
        elif calendar_id ==2:
            cm.get_started(values)
            menu_id='O2'
        else:
            return None

        # Создать новую клавиатуру
        text = f'{self.trans[46]}'
        reply_markup = self.bt.build_footer_buttons(menu_id=menu_id, response=call)
        return self._build_keyboard(text, reply_markup)

    """---------------------------ОБЩАЯ__СТАТИСТИКА---------------------------"""
    # Общая статистика
    def build_common_stats_kb(self, response):
        text = f'{self.trans[28]}'
        reply_markup = self.bt.build_common_stats(response)
        return self._build_keyboard(text, reply_markup)

    def build_books_nb_kb(self, response):
        text = f'{self.trans[29]}: '
        text += cm.select_books()
        reply_markup = self.bt.build_footer_buttons(menu_id='C1', response=response)
        return self._build_keyboard(text, reply_markup)

    def build_read_books_nb_kb(self, response):
        text = f'{self.trans[30]}: '
        text += cm.select_count_read_books()
        reply_markup = self.bt.build_footer_buttons(menu_id='C1', response=response)
        return self._build_keyboard(text, reply_markup)

    """---------------------------ПО КАТЕГОРИЯМ---------------------------"""
    def build_stats_by_category_kb(self, response):
        text = f'{self.trans[31]}'
        reply_markup = self.bt.build_stats_by_category(response)
        return self._build_keyboard(text, reply_markup)

    def build_books_by_category_kb(self, response):
        text = f'{self.trans[32]}:\n'
        text += cm.select_books_by_category()
        reply_markup = self.bt.build_footer_buttons(menu_id='C2', response=response)
        return self._build_keyboard(text, reply_markup)

    def build_read_by_category_kb(self, response):
        text = f'{self.trans[33]}:\n'
        text += cm.select_read_by_category()
        reply_markup = self.bt.build_footer_buttons(menu_id='C2', response=response)
        return self._build_keyboard(text, reply_markup)

    def build_average_data_by_category_kb(self, response):
        text = f'{self.trans[34]}м:\n'
        text += cm.select_average_data_by_category()
        reply_markup = self.bt.build_footer_buttons(menu_id='C2', response=response)
        return self._build_keyboard(text, reply_markup)

    """---------------------------ПО ЯЗЫКАМ---------------------------"""
    def build_stats_by_language_kb(self, response):
        text = f'{self.trans[35]}'
        reply_markup = self.bt.build_stats_by_language(response)
        return self._build_keyboard(text, reply_markup)

    def build_books_by_language_kb(self, response):
        text = f'{self.trans[36]}:\n'
        text += cm.select_books_by_language()
        reply_markup = self.bt.build_footer_buttons(menu_id='C3', response=response)
        return self._build_keyboard(text, reply_markup)

    def build_read_by_language_kb(self, response):
        text = f'{self.trans[37]}:\n'
        text += cm.select_read_by_language()
        reply_markup = self.bt.build_footer_buttons(menu_id='C3', response=response)
        return self._build_keyboard(text, reply_markup)

    """---------------------ПО КАТЕГОРИЯМ И ЯЗЫКАМ---------------------"""
    def build_stats_by_category_and_lang_kb(self, response):
        text = f'{self.trans[38]}'
        reply_markup = self.bt.build_stats_by_category_and_lang(response)
        return self._build_keyboard(text, reply_markup)

    def build_books_by_category_and_lang_kb(self, response):
        text = f'{self.trans[39]}:\n'
        text += cm.select_books_by_category_and_language()
        reply_markup = self.bt.build_footer_buttons(menu_id='C4', response=response)
        return self._build_keyboard(text, reply_markup)

    """---------------------------ЧТО ПОЧИТАТЬ---------------------------"""
    def build_to_read_kb(self, response):
        text = f'{self.trans[20]}'
        reply_markup = self.bt.build_to_read(response)
        return self._build_keyboard(text, reply_markup)

    # Описание при получении команды /help или /info
    def build_info_text(self, response):
        user_id = response.from_user.id
        description = self.trans[58]
        version = VERSION
        available_languagues = ', '.join(AVAILABLE_LANGUAGUES)
        access_level = get_user_access_level(user_id)

        text = f'<b>{self.trans[54]}:</b> {description}\n' \
               f'<b>{self.trans[55]}:</b> {version}\n' \
               f'<b>{self.trans[56]}:</b> {available_languagues}\n' \
               f'<b>{self.trans[57]}:</b> {access_level}'

        return text

    # Ответ на текстовое сообщение пользователя
    def build_text_on_text_call(self):
        text = f'{self.trans[27]}'

        return text

    # Проверка на соответствие календарю
    def cal_func(self, calendar_id):
        return self.calendars.func(calendar_id)

    # Проверка на соответствие пагинации
    def pag_func(self, pagin_id):
        return self.paginations.func(pagin_id)


