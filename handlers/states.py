from telebot.asyncio_handler_backends import State, StatesGroup


class States(StatesGroup):
    book_id = State()
    started = State()
    finished = State()