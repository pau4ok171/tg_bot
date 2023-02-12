import random
from datetime import date

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.keyboard import Keyboard
from builders.static import DAYS_OF_WEEK, MONTHS, STEP
import schemas

import calendar
from dateutil.relativedelta import relativedelta
from calendar import monthrange
calendar.setfirstweekday(calendar.MONDAY)


class Calendar(Keyboard):
    def __init__(self, bot=None, bt=None, db=None, cm=None, bot_cm=None, calendar_id=0):
        super().__init__(bot, bt, db, cm, bot_cm)
        self.calendar_id = calendar_id
        self.handler = f'calendar_{calendar_id}'
        self.prev_button = '<<'
        self.middle_button = ' '
        self.next_button = '>>'
        self.empty_nav_button = '×'
        self.year_size = 2
        self.month_size = 3
        self.day_size = 7

    def build(self, params=None) -> schemas.Keyboard:
        params = params or self._build_params()
        step = params['step']
        buttons = None

        if step == 'YEAR':
            buttons = self._build_years()
        elif step == 'MONTH':
            buttons = self._build_months()
        elif step == 'DAY':
            buttons = self._build_days()

        n_buttons = self._build_navigation(params)
        f_buttons = self._build_footer()
        buttons.append(n_buttons)
        buttons.append(f_buttons)

        # Keyboard
        text = f'{self.trans[42]} {STEP[self.lang]["y"]}'
        reply_markup = InlineKeyboardMarkup(buttons)
        kb = self._build_keyboard(text, reply_markup)
        return kb

    def _build_callback(self, name):
        name = name or 'test'
        step = 'test'
        year = 'test'
        month = 'NULL'
        day = 'NULL'
        salt = str(random.randint(1, int(1e18)))
        callback = '&'.join((self.handler, name, step, year, month, day, salt))
        return callback

    def _build_years(self) -> list[list[InlineKeyboardButton]]:
        # Years
        size = 2
        text = 'Выберите год'
        years = [2021, 2022, 2023, 2024]
        buttons = [[InlineKeyboardButton(text=year, callback_data='year') for year in years]]
        buttons = [buttons[0][i:i + size] for i in range(0, len(buttons[0]), size)]

        return buttons

    def _build_months(self) -> list[list[InlineKeyboardButton]]:
        # Months
        size = 3
        text = 'Выберите месяц'
        MONTHS = ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]
        buttons = [[InlineKeyboardButton(text=month, callback_data='month') for month in MONTHS]]
        buttons = [buttons[0][i:i + size] for i in range(0, len(buttons[0]), size)]

        return buttons

    def _build_days(self) -> list[list[InlineKeyboardButton]]:
        # Days
        size = 7
        text = 'Выберите день'
        DAYS_OF_WEEK = ["П", "В", "С", "Ч", "П", "С", "В"]
        days = [i for i in range(1, 32)]
        days += DAYS_OF_WEEK
        buttons = [[InlineKeyboardButton(text=day, callback_data='day') for day in days]]
        buttons = [buttons[0][i:i + size] for i in range(0, len(buttons[0]), size)]

        return buttons

    def _build_navigation(self, params) -> list[InlineKeyboardButton]:
        # Navigation
        n_buttons = {'back': '<<', 'empty': ' ', 'next': '>>'}
        callback = {self._build_callback(k): v for k, v in n_buttons.items()}

        n_buttons = [InlineKeyboardButton(
            text=v,
            callback_data=k) for k, v in callback.items()]

        return n_buttons

    def _build_footer(self) -> list[InlineKeyboardButton]:
        # Footer
        f_buttons = {'return': 'Назад', 'home': 'Домой'}
        f_buttons = [InlineKeyboardButton(
            text=v,
            callback_data=k) for k, v in f_buttons.items()]

        return f_buttons

    def _build_params(self) -> dict:
        params = {
            'handler': f'{self.handler}',
            'name': 'choice',
            'step': 'YEAR',
            'year': 'NULL',
            'month': 'NULL',
            'day': 'NULL',
            'salt': str(random.randint(1, int(1e18)))
        }

        return params

    def func(self):
        def validation(call) -> bool:
            return call.data.startswith(self.handler)

        return validation

    def process(self):
        pass