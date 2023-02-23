from telebot import types
from handlers.states import BookState


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

    async def reset_state_data(self, response, state_id):
        # Открыть состояние id книги
        lvl = await self._set_state(response, state_id)

        # Отчистить сохраненные состояния в памяти
        async with self.bot.retrieve_data(
                response.message.from_user.id,
                response.message.chat.id
        ) as data:
            data[f'{lvl}_book_id'] = None
            data[f'{lvl}_date'] = None

    async def set_book_id(self, response, book_id, state_id):
        # Открыть состояние id книги
        lvl = await self._set_state(response, state_id)

        # Сохранить состояние id книги в память
        async with self.bot.retrieve_data(
                response.message.from_user.id,
                response.message.chat.id
        ) as data:
            data[f'{lvl}_book_id'] = book_id

    async def set_date(self, res, response, state_id):
        # Открыть состояние id книги
        lvl = await self._set_state(response, state_id)
        try:
            # Сохранить состояние finished в память
            # и сформировать кортеж для отправки в бд
            async with self.bot.retrieve_data(
                    response.message.from_user.id,
                    response.message.chat.id
            ) as data:
                data[f'{lvl}_date'] = res
                values = (data[f'{lvl}_date'], int(data[f'{lvl}_book_id']))
        except Exception as e:
            print(e)
            await self.send_message(
                response,
                'Данные устарели. Пожалуйста, повторите запрос.'
            )
            return None

        return values

    async def get_data(self, response, state_id):
        # Открыть состояние id книги
        lvl = await self._set_state(response, state_id)

        # Сохранить состояние f/s в память
        # и сформировать кортеж для отправки в бд
        async with self.bot.retrieve_data(
                response.message.from_user.id,
                response.message.chat.id
        ) as data:
            values = (data[f'{lvl}_date'], int(data[f'{lvl}_book_id']))

        return values

    async def retrieve_date(self, response, state_id):
        # Открыть состояние id книги
        lvl = await self._set_state(response, state_id)

        async with self.bot.retrieve_data(
                response.message.from_user.id,
                response.message.chat.id
        ) as data:
            data[f'{lvl}_date'] = None
            book_id = data[f'{lvl}_book_id']

        return book_id

    async def _set_state(self, response, state_id):
        if state_id == 1:
            state = BookState.f_book_id
            lvl = 'f'
        elif state_id == 2:
            state = BookState.s_book_id
            lvl = 's'
        else:
            return None

        # Открыть состояние id книги
        await self.bot.set_state(
            response.message.from_user.id,
            state,
            response.message.chat.id
        )

        return lvl