from functools import wraps
import config
from data_logging import LoggingManager


ADMINS = config.admins
REGISTERED = config.registered
ALLOWED_ID = config.allowed_id

lg = LoggingManager()


def recognize_user(user_id):
    return user_id in ALLOWED_ID

def recognize_admin(user_id):
    return user_id in ADMINS

def is_admin(message):
    user_id = message.from_user.id
    return user_id in ADMINS


def private_access(bot):
    def deco_restrict(func):
        @wraps(func)
        async def func_restrict(message, *args, **kwargs):
            user_id = message.from_user.id
            username = message.from_user.first_name

            if recognize_user(user_id):
                return await func(message, *args, **kwargs)
            else:
                lg.log_message(message)
                await bot.send_message(message.from_user.id,
                    text=f'Я тебя пока не знаю, {username}:(\n Мне нужно разрешение от папы...')

        return func_restrict

    return deco_restrict

def private_admin_access(bot):
    def deco_restrict(func):

        @wraps(func)
        async def func_restrict(message, *args, **kwargs):
            user_id = message.from_user.id
            if recognize_admin(user_id):
                return await func(message, *args, **kwargs)
            else:
                lg.log_message(message)
                await bot.send_message(message.from_user.id,
                                       text=f'Э! КАК ТЫ СЮДА ПОПАЛ!')

        return func_restrict

    return deco_restrict

def get_user_access_level(user_id):
    if user_id in ADMINS:
        return 'admin'
    elif user_id in REGISTERED:
        return 'registered'
    else:
        return 'non-registered'