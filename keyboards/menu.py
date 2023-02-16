from telebot import types
import config
from private_access import get_user_access_level
from handlers.states import StateManager
import math

from keyboards.keyboard import Keyboard
from command import CommandManager


VERSION = config.version
AVAILABLE_LANGUAGUES = config.available_languagues


cm = CommandManager()
st = StateManager()


class MenuManager(Keyboard):
    def __init__(self, bot, bt, calendars, paginations):
        # Инициализация родительского класса
        super().__init__()

        self.bot = bot
        self.bt = bt
        self.calendars = calendars
        self.paginations = paginations

    async def set_menu_commands(self):
        """
        Задать базовые команды для тг бота
        """
        await self.bot.set_my_commands([
            types.BotCommand('/start', 'starter'),
            types.BotCommand('/help', 'helper'),
            types.BotCommand('info', 'informer')
        ])

    def build_start_menu_kb(self, response):
        text = f'{self.trans[24]}, <b>{response.from_user.first_name}!</b> {self.trans[25]}!\n{self.trans[26]}'
        reply_markup = self.bt.build_start_menu(response)
        return self._build_keyboard(text, reply_markup)

    def build_common_stats_kb(self, response):
        text = f'{self.trans[28]}'
        reply_markup = self.bt.build_common_stats(response)
        return self._build_keyboard(text, reply_markup)

    def build_book_management_kb(self, response):
        text = f'{self.trans[48]}'
        reply_markup = self.bt.build_books_management(response)
        return self._build_keyboard(text, reply_markup)

    def build_admin_panel_kb(self, response):
        text = f'{self.trans[23]}'
        reply_markup = self.bt.build_admin_panel(response)
        return self._build_keyboard(text, reply_markup)

    def build_pagin_finished_kb(self):
        last_page = math.ceil(int(cm.select_books_nb_non_read()) / 10)
        text = f'{self.trans[50]} 1 {self.trans[51]} {last_page}'
        reply_markup = self.paginations.build_pagin_finished_reply(level=1)
        return self._build_keyboard(text, reply_markup)

    def build_pagin_started_kb(self):
        pass

    def build_pagin_top_kb(self):
        pass

    def build_calendar_clf_rb(self, response):
        # Найти id книги в полученной data
        params = self.bt.process_callback_data(response)
        book_id = params['data']['id']

        # Reset машины состояния
        st.reset_state_data(self.bot, response)

        # Сохранить состояние id книги в память
        st.set_book_id(self.bot, response, book_id)

        # Задать минимальную дату для первого календаря
        self.calendars.set_min_date_clf(cm.select_started_by_id(book_id))

        # Построить календарь
        kb, chosen_date = self.calendars.build_calendar_clf_kb()

        return kb

    def build_calendar_cls_rb(self, response):
        # Найти id книги в полученной data
        params = self.bt.process_callback_data(response)
        book_id = params['data']['id']

        # Reset машины состояния
        st.reset_state_data(self.bot, response)

        # Сохранить состояние id книги в память
        st.set_book_id(self.bot, response, book_id)

        # Построить календарь
        kb, chosen_date = self.calendars.build_calendar_clf_kb()

        return kb

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

    # Текст для ответа на текстовое сообщение пользователя
    def build_text_on_text_call(self):
        text = f'{self.trans[27]}'

        return text



