from telebot import types
from handlers.states import FBookState, SBookState, TBookState, UserState


TRANSACTIONS = {
    1: {'transaction_id': 'f_book_id', 'date': 'f_date_id'}, # f
    2: {'transaction_id': 's_book_id', 'date': 's_date_id'}, # s
    3: {'transaction_id': 't_book_id', 'genre': 't_genre', 'lang': 't_lang'}, # t
    4: {'transaction_id': 'user_id', 'access_level': 'user_new_access_level'}, # u
}

class TelebotCommandsManager:
    def __init__(self, bot):
        self.bot = bot

    async def send_message(self, response, text, reply_markup=None):

        await self.bot.send_message(
            response.from_user.id,
            text,
            reply_markup=reply_markup)

    async def edit_message(self, response, text, reply_markup=None):

        await self.bot.edit_message_text(
            text,
            response.from_user.id,
            response.message.id,
            reply_markup=reply_markup
        )

    # Задать базовое меню команд
    async def set_menu_commands(self):
        """
        Задать базовые команды для тг бота
        """
        await self.bot.set_my_commands([
            types.BotCommand('/start', 'starter'),
            types.BotCommand('/help', 'helper'),
            types.BotCommand('info', 'informer')
        ])

    async def delete_state(self, response, state_id):
        # Открыть состояние id книги
        await self._set_state(response, state_id)

        # Удалить state
        await self.bot.delete_state(response.message.from_user.id)

    async def set_transaction_id(self, response, transaction_id, state_id):
        # Открыть состояние id книги
        await self._set_state(response, state_id)

        # Сохранить состояние id книги в память
        async with self.bot.retrieve_data(response.message.from_user.id) as data:
            data[TRANSACTIONS[state_id]['transaction_id']] = transaction_id

    async def set_date(self, res, response, state_id):
        # Открыть состояние id книги
        await self._set_state(response, state_id)

        # Сохранить состояние finished в память
        async with self.bot.retrieve_data(response.message.from_user.id) as data:
            data[TRANSACTIONS[state_id]['date']] = res

    async def get_data(self, response, state_id):
        # Открыть состояние id книги
        await self._set_state(response, state_id)
        try:
            # Сохранить состояние f/s в память
            # и сформировать кортеж для отправки в бд
            async with self.bot.retrieve_data(response.message.from_user.id) as data:
                values = (
                    data[TRANSACTIONS[state_id]['date']],
                    int(data[TRANSACTIONS[state_id]['transaction_id']])
                )

        except Exception as e:
            print(e)
            await self.send_message(
                response,
                'Данные устарели. Пожалуйста, повторите запрос.'
            )
            return None

        return values

    async def retrieve_date(self, response, state_id):
        # Открыть состояние id книги
        await self._set_state(response, state_id)

        async with self.bot.retrieve_data(response.message.from_user.id) as data:
            data[TRANSACTIONS[state_id]['date']] = None
            book_id = int(data[TRANSACTIONS[state_id]['transaction_id']])

        return book_id

    async def get_user_id(self, response, state_id):
        # Открыть состояние id книги
        await self._set_state(response, state_id)

        async with self.bot.retrieve_data(response.message.from_user.id) as data:
            user_id = int(data[TRANSACTIONS[state_id]['transaction_id']])

        return user_id

    async def set_access_level(self, response, access_level, state_id):
        # Открыть состояние id книги
        await self._set_state(response, state_id)

        # Сохранить состояние finished в память
        async with self.bot.retrieve_data(response.message.from_user.id) as data:
            data[TRANSACTIONS[state_id]['access_level']] = access_level

    async def get_user_data(self, response, state_id) -> tuple | None:
        # Открыть состояние id книги
        await self._set_state(response, state_id)
        try:
            # Сформировать кортеж для отправки в бд
            async with self.bot.retrieve_data(response.message.from_user.id) as data:
                values = (
                    data[TRANSACTIONS[state_id]['access_level']],
                    data[TRANSACTIONS[state_id]['transaction_id']]
                )

        except Exception as e:
            print(e)
            await self.send_message(
                response,
                'Данные устарели. Пожалуйста, повторите запрос.'
            )
            return None

        return values

    async def _set_state(self, response, state_id):
        if state_id == 1:
            state = FBookState
        elif state_id == 2:
            state = SBookState
        elif state_id == 3:
            state = TBookState
        elif state_id == 4:
            state = UserState
        else:
            return

        # Открыть состояние id книги
        await self.bot.set_state(response.message.from_user.id, state)

    async def t_test(self, response, res, state_id):
        await self.bot.set_state(response.message.from_user.id, TBookState)
        async with self.bot.retrieve_data(response.message.from_user.id) as data:
            data[TRANSACTIONS[state_id]['transaction_id']] = res
            print(data)
        print(res)

    async def u_test(self, response, res, state_id):
        pass