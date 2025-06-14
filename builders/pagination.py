from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import math
import schemas
from telebot import util
from keyboards.keyboard import Keyboard
from commands import CommandManager


NEXT_STEP = {'TRANSACTION': 'CHOSEN', 'PAGE': 'TRANSACTION'}
PREV_STEP = {'TRANSACTION': 'PAGE', 'PAGE': 'TRANSACTION'}

cm = CommandManager()


class TelegramPagination(Keyboard):
    def __init__(self, pagin_id: int=0, return_button: int=None):
        super().__init__()

        self.cm = cm
        self.return_button = return_button

        self.pagin_id = pagin_id
        self.handler = 'pagination'
        self.handler_id = f'{self.handler}_{self.pagin_id}'
        self.date = datetime.strftime(datetime.now().date(), '%d%m%Y')


        self.prev_button = '<<'
        self.next_button = '>>'
        self.first_button = '<<<'
        self.last_button = '>>>'
        self. empty_nav_button = '×'
        self.empty_page_button = ' '
        self.max_page_buttons = 42
        self.transaction_by_page = 10
        self.transaction_size = 1
        self.page_size = 7
        self.nav_size = 5
        self.footer_size = 3

        # Задать кол-во страниц для транзакций
        self.transaction_last_page = math.ceil(cm.select_transaction_nb_for_pagin(self.pagin_id) / self.transaction_by_page)
        # Задать кол-во страниц для меню 2-ого уровня.
        self.page_last_page = math.ceil(self.transaction_last_page / self.max_page_buttons)

    def build(self, call, page:int =1, params: dict=None) -> tuple[schemas.Keyboard | None, int | None]:
        self.set_user_lang(call)

        if not params: params = self._build_params()

        step = params['step']
        if step == 'TRANSACTION':
            buttons = self._build_transactions(page)
        elif step == 'PAGE':
            buttons = self._build_pages(page)
        elif step == 'CHOSEN':
            response = int(params['data'])
            return None, response
        else:
             return None, None

        # Navigation
        nav_buttons = self._build_navigation(page, params)
        # Footer
        f_buttons = self._build_footer()

        if step == 'TRANSACTION':
            last_page = self.transaction_last_page
        elif step == 'PAGE':
            last_page = self.page_last_page
        else:
            last_page = None

        # Keyboard
        text = f'{self.trans[50]} {page} {self.trans[51]} {last_page}'
        reply_markup = InlineKeyboardMarkup(buttons + nav_buttons + f_buttons)

        kb = self._build_keyboard(text, reply_markup)

        return kb, None

    def _build_callback(self, action, step, transaction_id=None, current_page=None) -> str:
        if transaction_id:
            data = transaction_id
        elif current_page:
            data = current_page
        else:
            data = util.generate_random_token()

        callback = '&'.join([self.handler_id, action, step, str(data)])

        return callback

    def _build_params(self, call=None) -> dict:
        """
        Извлечь данные из callback и сформировать params если он получен.
        Иначе сформировать новый params.
        """
        if call:
            params = call.data.split('&')
            params = dict(
                zip(['handler_id', 'action', 'step', 'data'][:len(params)], params))
        else:
            params = {
                'handler_id': f'{self.handler_id}',
                'action': 'choice',
                'step': 'TRANSACTION',
            }

        return params

    def _build_transactions(self, page) -> list[list[InlineKeyboardButton]]:
        # Вернуть из бд набор из книг
        skip_page = (page - 1) * 10

        transactions = self.cm.select_transactions_for_pagin(pagin_id=self.pagin_id, values=(skip_page,))

        text = [' '.join(f'{k}: {v}' for k, v in transaction.items()) for transaction in transactions]
        id_list = [transaction['id'] for transaction in transactions]

        callback = [
            self._build_callback(
                action='choice',
                step='TRANSACTION',
                transaction_id=transaction_id
            ) for transaction_id in id_list
        ]

        buttons = self._build_buttons(
            text=text,
            callback=callback,
            size=self.transaction_size
        )

        return buttons

    def _build_pages(self, page) -> list[list[InlineKeyboardButton]]:

        first = 1 + (self.max_page_buttons * (page-1))
        last = self.max_page_buttons * page

        text = [
            i if i <= self.transaction_last_page else self.empty_page_button for i in range(first, last + 1)
        ]

        callback = [
            self._build_callback(
                action='choice' if i <= self.transaction_last_page else 'empty',
                step='PAGE',
                current_page=i
            ) for i in range(first, last+1)
        ]

        buttons = self._build_buttons(
            text=text,
            callback=callback,
            size=self.page_size,
        )

        return buttons

    def _build_navigation(self, page, params) -> list[list[InlineKeyboardButton]]:
        step = params['step']

        if step == 'TRANSACTION':
            last_page = self.transaction_last_page
        elif step == 'PAGE':
            last_page = self.page_last_page
        else:
            last_page = None

        prev_exists = (page != 1)
        next_exists = (page != last_page)

        text = [
            self.first_button if prev_exists else self.empty_nav_button,
            self.prev_button if prev_exists else self.empty_nav_button,
            page,
            self.next_button if next_exists else self.empty_nav_button,
            self.last_button if next_exists else self.empty_nav_button,
        ]

        actions = [
            'first' if prev_exists else 'empty_first',
            'prev' if prev_exists else 'empty_prev',
            'middle',
            'next' if next_exists else 'empty_next',
            'last' if next_exists else 'empty_last',
        ]

        callback = [
            self._build_callback(
                action,
                step=step,
                current_page=page,

            ) for action in actions

        ]

        n_buttons = self._build_buttons(
            text=text,
            callback=callback,
            size=self.nav_size,
        )

        return n_buttons

    def _build_footer(self) -> list[list[InlineKeyboardButton]]:
        # Создать лист нижних кнопок
        buttons = [self.return_button, 10026]

        f_buttons: dict = self.get_buttons_by_id(buttons, lang=self.lang)

        text = list(f_buttons.values())
        callback = list(f_buttons.keys())

        f_buttons: list = self._build_buttons(
            text=text,
            callback=callback,
            size=self.footer_size
        )

        return f_buttons

    # noinspection PyTypeChecker
    @staticmethod
    def func(pagin_id) -> bool:
        def validation(call) -> bool:
            start = f'pagination_{pagin_id}'
            return call.data.startswith(start)
        return validation

    def process(self, call) -> tuple[schemas.Keyboard | None, int | None]:
        params = self._build_params(call)

        action = params['action']
        step = params['step']
        page = int(params['data'])

        if action == 'choice':
            params['step'] = NEXT_STEP[step]
            page = page
            diff = 0
        elif action == 'first':
            page = 1
            diff = 0
        elif action == 'prev':
            diff = -1
        elif action == 'middle':
            params['step'] = PREV_STEP[step]
            page = 1
            diff = 0
        elif action == 'next':
            page = page
            diff = 1
        elif action == 'last':
            page = self.transaction_last_page
            diff = 0
        else:
            return None, None

        return self.build(call, page=page+diff, params=params)

