from telebot.asyncio_handler_backends import State, StatesGroup


class States(StatesGroup):
    book_id = State()
    started = State()
    finished = State()

class StateManager:
    @staticmethod
    async def reset_state_data(bot, response):
        # Отчистить сохраненные состояния в памяти
        await bot.delete_state(response.message.from_user.id, response.message.id)

        # Открыть состояние id книги
        await bot.set_state(
            response.message.from_user.id,
            States.book_id,
            response.message.chat.id
        )

    @staticmethod
    async def set_book_id(bot, res, book_id):
        # Сохранить состояние id книги в память
        async with bot.retrieve_data(res.message.from_user.id, res.message.chat.id) as data:
            data['book_id'] = book_id