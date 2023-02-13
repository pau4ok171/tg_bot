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
GOTO = {'YEAR': 'MONTH', 'MONTH': 'DAY', 'DAY': 'CHOSEN'}


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
            buttons = self._build_months(params)
        elif step == 'DAY':
            buttons = self._build_days(params)

        n_buttons = self._build_navigation(params)
        f_buttons = self._build_footer()
        buttons.append(n_buttons)
        buttons.append(f_buttons)

        # Keyboard
        text = f'{self.trans[42]} {STEP[self.lang][step.lower()]}'
        reply_markup = InlineKeyboardMarkup(buttons)
        kb = self._build_keyboard(text, reply_markup)
        return kb

    def _build_callback(self, action, step, date=None):
        if date:
            date = list(map(str, date.timetuple()[:3]))
        else:
            date = []
        params = [self.handler, action, step] + date

        callback = '&'.join(params)
        return callback

    def _build_years(self) -> list[list[InlineKeyboardButton]]:
        # Years
        size = self.year_size
        years = [2021, 2022, 2023, 2024]
        callback = [self._build_callback('choice', 'YEAR', self._get_date(year, 1, 1)) for year in years]
        buttons = {k: v for k, v in dict(zip(callback, years)).items()}
        buttons = [[InlineKeyboardButton(text=v, callback_data=k) for k, v in buttons.items()]]
        buttons = [buttons[0][i:i + size] for i in range(0, len(buttons[0]), size)]

        return buttons

    def _get_date(self, year, month, day):
        return date(year, month, day)

    def _build_months(self, params) -> list[list[InlineKeyboardButton]]:
        # Months
        size = self.month_size
        months = MONTHS[self.lang]
        year = int(params['year'])
        callback = [self._build_callback('choice', 'MONTH', self._get_date(year, month, 1)) for month in range(1,13)]
        buttons = {k: v for k, v in dict(zip(callback, months)).items()}
        buttons = [[InlineKeyboardButton(text=v, callback_data=k) for k, v in buttons.items()]]
        buttons = [buttons[0][i:i + size] for i in range(0, len(buttons[0]), size)]

        return buttons

    def _build_days(self, params) -> list[list[InlineKeyboardButton]]:
        # Days
        year = int(params['year'])
        month = int(params['month'])
        size = self.day_size
        days_of_week = DAYS_OF_WEEK[self.lang]
        days = [i for i in range(1, 32)]
        callback_of_week = [self._build_callback('empty', 'EMPTY', self._get_date(year, month, i)) for i, days in enumerate(days_of_week, start=1)]
        callback = [self._build_callback('choice', 'DAY', self._get_date(year, month, day)) for day in days]
        callback = callback_of_week + callback
        days = days_of_week + days
        buttons = {k: v for k, v in dict(zip(callback, days)).items()}
        buttons = [[InlineKeyboardButton(text=v, callback_data=k) for k, v in buttons.items()]]
        buttons = [buttons[0][i:i + size] for i in range(0, len(buttons[0]), size)]

        return buttons

    def _build_navigation(self, params) -> list[InlineKeyboardButton]:
        # Navigation
        n_buttons = {'back': '<<', 'empty': ' ', 'next': '>>'}
        callback = {self._build_callback(k, 'YEAR', self._get_date(2023, 1, 1)): v for k, v in n_buttons.items()}

        n_buttons = [InlineKeyboardButton(
            text=v,
            callback_data=k) for k, v in callback.items()]

        return n_buttons

    def _build_footer(self) -> list[InlineKeyboardButton]:
        # Footer 10001 or 10030, 10002
        f_buttons = {'return': self.trans[3], 'home': self.trans[2]}
        f_buttons = [InlineKeyboardButton(
            text=v,
            callback_data=k) for k, v in f_buttons.items()]

        return f_buttons

    def _build_params(self, call=None) -> dict:
        """
        Извлечь данные из callback и сформировать params если он получен.
        Иначе сформировать новый params.
        """
        if call:
            params = call.data.split('&')
            params = dict(
                zip(['handler', 'action', 'step', 'year', 'month', 'day'][:len(params)], params))
        else:
            params = {
                'handler': f'{self.handler}',
                'action': 'choice',
                'step': 'YEAR'
            }

        return params

    def func(self):
        def validation(call) -> bool:
            return call.data.startswith(self.handler)

        return validation

    def process(self, call):
        params = self._build_params(call)
        action = params['action']
        step = params['step']

        print(params)
        if action == 'choice':
            params['step'] = GOTO[step]
            kb = self.build(params)
            print(kb)
        return kb

