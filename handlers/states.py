from telebot.asyncio_handler_backends import State, StatesGroup


class BookState(StatesGroup):
    f_book_id = State()
    f_date = State()
    s_book_id = State()
    s_date = State()


