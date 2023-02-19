from telebot.asyncio_handler_backends import State, StatesGroup


class Finished(StatesGroup):
    book_id = State()
    finished = State()

class Started(StatesGroup):
    book_id = State()
    started = State()

