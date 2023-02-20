from datetime import date
from telebot import util

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.keyboard import Keyboard
from builders.static import DAYS_OF_WEEK, MONTHS, STEP
import schemas
import calendar
from dateutil.relativedelta import relativedelta
from calendar import monthrange


# Задать понедельник первым днем недели
calendar.setfirstweekday(calendar.MONDAY)


NEXT_STEP = {'YEAR': 'MONTH', 'MONTH': 'DAY', 'DAY': 'CHOSEN'}
PREV_STEP = {'YEAR': 'EMPTY', 'MONTH': 'YEAR', 'DAY': 'MONTH'}


class Calendar(Keyboard):
    def __init__(
            self,
            calendar_id=0,
            max_date=None,
            min_date=None,
            current_date=None,
            footer_buttons=None
    ):
        super().__init__()

        if current_date is None: current_date = date.today()
        if max_date is None: max_date = date(2999, 12, 31)
        if min_date is None: min_date = date(1, 1, 1)

        self.handler = f'calendar_{calendar_id}'
        self.prev_button = '<<'
        self.next_button = '>>'
        self.empty_nav_button = '×'
        self.empty_date_button = ' '
        self.year_size = 2
        self.month_size = 3
        self.day_size = 7
        self.nav_size = 3
        self.footer_size = 2
        self.current_date = current_date
        self.max_date = max_date
        self.min_date = min_date
        self.ref_date = current_date
        self.footers_buttons = footer_buttons

    def build(self, call, params: dict=None, diff: int=0) -> tuple[schemas.Keyboard | None, date | None]:
        self.set_user_lang(call)

        if not params: params = self._build_params()

        step = params['step']

        if step == 'YEAR':
            buttons = self._build_years(diff)
        elif step == 'MONTH':
            buttons = self._build_months(params, diff)
        elif step == 'DAY':
            buttons = self._build_days(params, diff)
        elif step == 'CHOSEN':
            chosen_date = date(int(params['year']), int(params['month']), int(params['day']))
            return None, chosen_date
        else:
            return None, None

        # Navigation
        nav_buttons = self._build_navigation(params)
        # Footer
        f_buttons = self._build_footer()

        # Keyboard
        text = f'{self.trans[42]} {STEP[self.lang][step.lower()]}'
        reply_markup = InlineKeyboardMarkup(buttons + nav_buttons+ f_buttons)

        kb = self._build_keyboard(text, reply_markup)
        return kb, None

    def _build_callback(self, action, step, current_date=None, token=None) -> str:
        """
        :param action: choice, nav_back, nav_middle, nav_next, empty
        :param step: YEAR, MONTH, DAY, CHOSEN
        :param current_date: datetime.date
        :param token:
        Токен необходим в случае если мы задаем callback для пустых элементов
        с целью сделать объекты уникальными и избежать удаления этих объектов
        как дубликатов.
        :return:
        Возвращает строку формата: handler&action&step&year&month&day
        или формата handler&action&step&token если current_date=None.
        """
        if current_date:
            data = list(map(str, current_date.timetuple()[:3]))
        elif token:
            data = [token]
        else:
            data = []

        callback = '&'.join([self.handler, action, step] + data)

        return callback

    def _build_years(self, diff: int=0) -> list[list[InlineKeyboardButton]]:
        # Years
        size = self.year_size
        self.ref_date += relativedelta(years=diff*4)
        self.current_date += relativedelta(years=diff*4)
        ref_year = self.ref_date.year

        years = [
            year if self._valid_date('YEAR', date(year, 1, 1)) else self.empty_date_button
            for year in range(ref_year-1, ref_year+3)
        ]

        callback = [
            self._build_callback(
                'choice' if self._valid_date('YEAR', date(year, 1, 1)) else 'empty',
                'YEAR',
                date(year, 1, 1),
                token=util.generate_random_token()
            ) for year in range(ref_year-1, ref_year+3)
        ]

        buttons = self._build_buttons(
            text=years,
            callback=callback,
            size=size,
        )

        return buttons

    def _build_months(self, params, diff=0) -> list[list[InlineKeyboardButton]]:
        # Months
        size = self.month_size
        year = int(params['year'])

        self.current_date = date(year, 1, 1) + relativedelta(years=diff)

        year, month, day = self.current_date.timetuple()[:3]

        months = [
            MONTHS[self.lang][month-1]
            if self._valid_date('MONTH', date(year, month, day))
            else self.empty_date_button
            for month in range(1,13)
        ]

        callback = [
            self._build_callback(
                'choice' if self._valid_date('MONTH', date(year, month, day)) else 'empty',
                'MONTH',
                date(year, month, 1),
                token=util.generate_random_token()
            ) for month in range(1,13)
        ]

        buttons = self._build_buttons(
            text=months,
            callback=callback,
            size=size,
        )

        return buttons

    def _build_days(self, params, diff=0) -> list[list[InlineKeyboardButton]]:
        # Days
        year = int(params['year'])
        month = int(params['month'])
        self.current_date = date(year, month, 1) + relativedelta(months=diff)

        year, month, day = self.current_date.timetuple()[:3]

        size = self.day_size
        days_of_week = DAYS_OF_WEEK[self.lang]

        cl = calendar.monthcalendar(year, month)
        if len(cl) == 5:  cl.append([0, 0, 0, 0, 0, 0, 0])

        days = [
            day
            if day != 0 and self._valid_date('DAY', date(year, month, day))
            else self.empty_date_button
            for week in cl for day in week
        ]

        callback_of_week = [
            self._build_callback(
                'empty',
                'DAY',
                token=util.generate_random_token()
            ) for _ in range(7)
        ]

        callback = [
            self._build_callback('choice' if day != self.empty_date_button else 'empty', 'DAY',
                date(year, month, day) if day != self.empty_date_button else None,
                token=util.generate_random_token()
            ) for day in days
        ]

        buttons = self._build_buttons(
            text=days_of_week + days,
            callback=callback_of_week + callback,
            size=size,
        )

        return buttons

    def _build_navigation(self, params) -> list[list[InlineKeyboardButton]]:
        # Navigation
        size = self.nav_size
        nav_middle = None
        prev_date = None
        next_date = None
        step = params['step']

        year, month, day = self.current_date.timetuple()[:3]

        if step == 'YEAR':
            nav_middle = ' '
            prev_date = self.ref_date + relativedelta(years=-2)
            next_date = self.ref_date + relativedelta(years=3)
        elif step == 'MONTH':
            nav_middle = year
            prev_date = self.current_date.replace(month=12) + relativedelta(years=-1)
            next_date = self.current_date.replace(month=1) + relativedelta(years=1)
        elif step == 'DAY':
            nav_middle = f'{MONTHS[self.lang][month - 1]} {year}'
            prev_date = self.current_date.replace(day=monthrange(year, month)[1]) + relativedelta(months=-1)
            next_date = self.current_date.replace(day=1) + relativedelta(months=1)

        prev_exists = self._valid_date(step, prev_date)
        next_exists = self._valid_date(step, next_date)

        text = [
            self.prev_button if prev_exists else self.empty_nav_button,
            nav_middle,
            self.next_button if next_exists else self.empty_nav_button,
        ]

        actions = [
            'nav_back' if prev_exists else 'empty_prev',
            'nav_middle',
            'nav_next' if next_exists else 'empty_next',
        ]

        callback = [
            self._build_callback(
                action,
                step,
                date(year, month, day)
            ) for action in actions
        ]

        n_buttons = self._build_buttons(
            text=text,
            callback=callback,
            size=size
        )

        return n_buttons

    def _build_footer(self) -> list[list[InlineKeyboardButton]]:
        # Footer 10001 or 10030
        size = self.footer_size

        buttons: list = self.footers_buttons

        f_buttons: dict = self.get_buttons_by_id(buttons, lang=self.lang)

        text = list(f_buttons.values())
        callback = list(f_buttons.keys())

        f_buttons: list = self._build_buttons(
            text=text,
            callback=callback,
            size=size
        )

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

    @staticmethod
    def func(calendar_id):
        def validation(call) -> bool:
            start = f'calendar_{calendar_id}'
            return call.data.startswith(start)

        return validation

    def process(self, call) -> tuple[schemas.Keyboard | None, date | None]:
        params = self._build_params(call)
        action = params['action']
        step = params['step']

        if action == 'choice':
            params['step'] = NEXT_STEP[step]
            kb, chosen_date = self.build(call, params)
        elif action == 'nav_back':
            kb, chosen_date = self.build(call, params, diff=-1)
        elif action == 'nav_next':
            kb, chosen_date = self.build(call, params, diff=+1)
        elif action == 'nav_middle':
            params['step'] = PREV_STEP[step]
            kb, chosen_date = self.build(call, params)
        else:
            return None, None

        return kb, chosen_date

    def _valid_date(self, step, d):
        if step == 'YEAR':
            return self.min_date.year <= d.year <= self.max_date.year
        elif step == 'MONTH':
            min_date = self.min_date.replace(day=1)
            max_date = self.max_date.replace(day=monthrange(self.max_date.year, self.max_date.month)[1])
            return min_date <= d <= max_date
        elif step == 'DAY':
            return self.min_date <= d <= self.max_date




