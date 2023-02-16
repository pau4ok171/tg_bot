from datetime import date
from telebot import util

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.keyboard import Keyboard
from builders.static import DAYS_OF_WEEK, MONTHS, STEP
import schemas

import calendar
from dateutil.relativedelta import relativedelta
from calendar import monthrange


calendar.setfirstweekday(calendar.MONDAY)


NEXT_STEP = {'YEAR': 'MONTH', 'MONTH': 'DAY', 'DAY': 'CHOSEN'}
PREV_STEP = {'YEAR': 'EMPTY', 'MONTH': 'YEAR', 'DAY': 'MONTH'}

class Calendar(Keyboard):
    def __init__(self, bot=None, bt=None, db=None, cm=None, bot_cm=None, menu=None, calendar_id=0, max_date=None, min_date=None, current_date=None):
        super().__init__(bot, bt, db, cm, bot_cm)

        if current_date is None: current_date = date.today()
        if max_date is None: max_date = date(2999, 12, 31)
        if min_date is None: min_date = date(1, 1, 1)

        self.menu = menu
        self.calendar_id = calendar_id
        self.handler = f'calendar_{calendar_id}'
        self.prev_button = '<<'
        self.next_button = '>>'
        self.empty_nav_button = '×'
        self.year_size = 2
        self.month_size = 3
        self.day_size = 7
        self.current_date = current_date
        self.max_date = max_date
        self.min_date = min_date
        self.ref_date = current_date

    def build(self, params=None, diff=None) -> tuple[schemas.Keyboard | None, date | None]:
        chosen_date = None
        kb = None
        params = params or self._build_params()
        step = params['step']

        if step == 'YEAR':
            buttons = self._build_years(diff)
        elif step == 'MONTH':
            buttons = self._build_months(params, diff)
        elif step == 'DAY':
            buttons = self._build_days(params, diff)
        elif step == 'CHOSEN':
            chosen_date = self._get_date(int(params['year']), int(params['month']), int(params['day']))
            return kb, chosen_date
        else:
            return None, None

        n_buttons = self._build_navigation(params)
        f_buttons = self._build_footer()
        buttons.append(n_buttons)
        buttons.append(f_buttons)

        # Keyboard
        text = f'{self.trans[42]} {STEP[self.lang][step.lower()]}'
        reply_markup = InlineKeyboardMarkup(buttons)

        kb = self._build_keyboard(text, reply_markup)
        return kb, chosen_date

    def _build_callback(self, action, step, current_date=None, token=None):
        if current_date:
            data = list(map(str, current_date.timetuple()[:3]))
        elif token:
            data = [token]
        else:
            data = []

        params = [self.handler, action, step] + data

        callback = '&'.join(params)
        return callback

    def _build_years(self, diff) -> list[list[InlineKeyboardButton]]:
        # Years
        size = self.year_size
        diff = diff or 0
        self.ref_date += relativedelta(years=diff*4)
        self.current_date = self.current_date + relativedelta(years=diff*4)

        year, month, day = self.ref_date.timetuple()[:3]
        years = [year if self._valid_date('YEAR', date(year, month, day)) else ' ' for year in range(year-1, year+3)]

        callback = [
            self._build_callback(
                'choice' if self._valid_date('YEAR', date(year, month, day)) else 'empty',
                'YEAR',
                current_date=self._get_date(year, 1, 1) if self._valid_date('YEAR', date(year, month, day)) else None,
                token=util.generate_random_token()
            ) for year in range(year-1, year+3)
        ]

        buttons = {k: v for k, v in dict(zip(callback, years)).items()}
        buttons = [[InlineKeyboardButton(text=v, callback_data=k) for k, v in buttons.items()]]
        buttons = [buttons[0][i:i + size] for i in range(0, len(buttons[0]), size)]

        return buttons

    def _get_date(self, year, month, day) -> date:
        return date(year, month, day)

    def _build_months(self, params, diff) -> list[list[InlineKeyboardButton]]:
        # Months
        size = self.month_size
        diff = diff or 0
        year = int(params['year'])

        self.current_date = self._get_date(year, 1, 1) + relativedelta(years=diff)

        year, month, day = self.current_date.timetuple()[:3]
        months = [MONTHS[self.lang][month-1] if self._valid_date('MONTH', date(year, month, day)) else ' ' for month in range(1,13)]

        callback = [
            self._build_callback(
                'choice' if self._valid_date('MONTH', date(year, month, day)) else 'empty',
                'MONTH',
                current_date=self._get_date(year, month, 1) if self._valid_date('MONTH', date(year, month, day)) else None,
                token=util.generate_random_token()
            ) for month in range(1,13)
        ]

        buttons = {k: v for k, v in dict(zip(callback, months)).items()}
        buttons = [[InlineKeyboardButton(text=v, callback_data=k) for k, v in buttons.items()]]
        buttons = [buttons[0][i:i + size] for i in range(0, len(buttons[0]), size)]

        return buttons

    def _build_days(self, params, diff) -> list[list[InlineKeyboardButton]]:
        # Days
        diff = diff or 0
        year = int(params['year'])
        month = int(params['month'])
        self.current_date = self._get_date(year, month, 1) + relativedelta(months=diff)

        year, month, day = self.current_date.timetuple()[:3]

        size = self.day_size
        days_of_week = DAYS_OF_WEEK[self.lang]

        cl = calendar.monthcalendar(year, month)
        if len(cl) == 5:  cl.append([0, 0, 0, 0, 0, 0, 0])
        days = [day if day != 0 and self._valid_date('DAY', date(year, month, day)) else ' ' for week in cl for day in week]

        callback_of_week = [self._build_callback('empty', 'EMPTY', token=util.generate_random_token()) for i in range(7)]

        callback = [
            self._build_callback(
                'choice' if day != ' ' else 'empty',
                'DAY',
                current_date=self._get_date(year, month, day) if day != ' ' else None,
                token=util.generate_random_token()
            ) for day in days
            ]

        days = days_of_week + days
        callback = callback_of_week + callback

        buttons = {k: v for k, v in dict(zip(callback, days)).items()}
        buttons = [[InlineKeyboardButton(text=v, callback_data=k) for k, v in buttons.items()]]
        buttons = [buttons[0][i:i + size] for i in range(0, len(buttons[0]), size)]

        return buttons

    def _build_navigation(self, params) -> list[InlineKeyboardButton]:
        # Navigation
        nav_middle = None
        prev_exists = None
        next_exists = None
        step = params['step']

        year, month, day = self.current_date.timetuple()[:3]
        print(self.current_date, self.ref_date)

        if step == 'YEAR':
            nav_middle = ' '
            prev_exists = self._valid_date(step, self.ref_date + relativedelta(years=-2))
            next_exists = self._valid_date(step, self.ref_date + relativedelta(years=3))
        elif step == 'MONTH':
            nav_middle = year
            prev_exists = self._valid_date(step, self.current_date.replace(month=12) + relativedelta(years=-1))
            next_exists = self._valid_date(step, self.current_date.replace(month=1) + relativedelta(years=1))
        elif step == 'DAY':
            nav_middle = f'{MONTHS[self.lang][month - 1]} {year}'
            prev_exists = self._valid_date(step, self.current_date.replace(day=monthrange(year, month)[1]) + relativedelta(months=-1))
            next_exists = self._valid_date(step, self.current_date.replace(day=1) + relativedelta(months=1))

        n_buttons = {
            'nav_back' if prev_exists else 'empty_prev' : '<<' if prev_exists else self.empty_nav_button,
            'nav_middle': nav_middle,
            'nav_next' if next_exists else 'empty_next' : '>>' if next_exists else self.empty_nav_button,
        }

        n_buttons = {
            self._build_callback(
                k,
                step,
                self._get_date(year, month, day)
            ): v for k, v in n_buttons.items()
        }

        n_buttons = [
            InlineKeyboardButton(
                text=v,
                callback_data=k
            ) for k, v in n_buttons.items()
        ]

        return n_buttons

    def _build_footer(self) -> list[InlineKeyboardButton]:
        # Footer
        return_button = None
        if self.calendar_id == 1:
            return_button = 10001
        elif self.calendar_id == 2:
            return_button = 10030
        buttons = [return_button, 10002]

        f_buttons: dict = self.bt.get_buttons_by_id(buttons, lang=self.lang)

        f_buttons: list = [InlineKeyboardButton(
            text=v,
            callback_data=k) for k, v in f_buttons.items()]

        return f_buttons

    def _build_params(self, call=None) -> dict:
        """
        Извлечь данные из callback и сформировать params если он получен.
        Иначе сформировать новый params.
        """
        year, month, day = self.current_date.timetuple()[:3]
        if call:
            params = call.data.split('&')
            params = dict(
                zip(['handler', 'action', 'step', 'year', 'month', 'day'][:len(params)], params))
        else:
            params = {
                'handler': f'{self.handler}',
                'action': 'choice',
                'step': 'YEAR',
                'year': year,
                'month': month,
                'day': day
            }

        return params

    def func(self):
        def validation(call) -> bool:
            return call.data.startswith(self.handler)

        return validation

    def process(self, call):
        kb = None
        chosen_date = None
        params = self._build_params(call)
        action = params['action']
        step = params['step']

        year = int(params['year'])
        month = int(params['month'])
        day = int(params['day'])

        if action == 'choice':
            params['step'] = NEXT_STEP[step]
            kb, chosen_date = self.build(params)
        elif action == 'nav_back':
            kb, chosen_date = self.build(params, diff=-1)
        elif action == 'nav_next':
            kb, chosen_date = self.build(params, diff=+1)
        elif action == 'nav_middle':
            params['step'] = PREV_STEP[step]
            kb, chosen_date = self.build(params)

        return kb, chosen_date

    def _valid_date(self, step, date):
        if step == 'YEAR':
            return self.min_date.year <= date.year <= self.max_date.year
        elif step == 'MONTH':
            min_date = self.min_date.replace(day=1)
            max_date = self.max_date.replace(day=monthrange(self.max_date.year, self.max_date.month)[1])
            return min_date <= date <= max_date
        elif step == 'DAY':
            return self.min_date <= date <= self.max_date


