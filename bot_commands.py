from telebot import types
from handlers.states import Started, Finished


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
        # Отчистить сохраненные состояния в памяти
        await self.bot.delete_state(response.message.from_user.id, response.message.id)

        if state_id == 1:
            st = Finished
        elif state_id == 2:
            st = Started
        else:
            return None

        # Открыть состояние id книги
        await self.bot.set_state(
            response.message.from_user.id,
            st.book_id,
            response.message.chat.id
        )

    async def set_book_id(self, response, book_id):
        # Сохранить состояние id книги в память
        async with self.bot.retrieve_data(
                response.message.from_user.id,
                response.message.chat.id
        ) as data:
            data['book_id'] = book_id

    async def set_date(self, res, call, calendar_id):
        if calendar_id == 1:
            st = Finished
            lvl = 'finished'
        elif calendar_id == 2:
            st = Started
            lvl = 'started'
        else:
            return None

        # Открыть состояние id книги
        await self.bot.set_state(
            call.message.from_user.id,
            st.book_id,
            call.message.chat.id
        )

        # Сохранить состояние finished в память
        # и сформировать кортеж для отправки в бд
        async with self.bot.retrieve_data(
                call.message.from_user.id,
                call.message.chat.id
        ) as data:
            data[lvl] = res
            values = (data[lvl], int(data['book_id']))

        return values

    async def retrieve_data(self, call, calendar_id):

        if calendar_id == 1:
            st = Finished
            lvl = 'finished'
        elif calendar_id == 2:
            st = Started
            lvl = 'started'
        else:
            return None

        # Сохранить состояние finished в память
        # и сформировать кортеж для отправки в бд
        async with self.bot.retrieve_data(
                call.message.from_user.id,
                call.message.chat.id
        ) as data:
            values = (data[lvl], int(data['book_id']))

        return values