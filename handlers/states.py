from telebot.asyncio_handler_backends import State, StatesGroup


class SBookState(StatesGroup):
    s_book_id = State()
    s_date = State()

class FBookState(StatesGroup):
    f_book_id = State()
    f_date = State()

class TBookState(StatesGroup):
    t_book_id = State()
    t_genre = State()
    t_lang = State()

class UserState(StatesGroup):
    user_id = State()
    user_new_access_level = State()


