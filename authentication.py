from functools import wraps
from data_logging import LoggingManager
from commands import CommandManager


ADMIN = ['admin']
ALLOWED_ID = ['admin', 'registered']

lg = LoggingManager()
cm = CommandManager()


class AuthentificationManager:
    @staticmethod
    def recognize_user(user_access_level, access_level):
        if access_level == 'admin':
            return user_access_level in ADMIN
        elif access_level == 'registered':
            return user_access_level in ALLOWED_ID

    def access_level_check(self, bot, access_level='registered'):
        def deco_restrict(func):
            @wraps(func)
            async def func_restrict(response, *args, **kwargs):
                user_id = response.from_user.id

                # Получить из unique_users бд список user_id
                unique_users: list = cm.select_unique_users()

                # Проверить есть ли пользователь в полученном списке
                if user_id in unique_users:
                    # Если да получить уровень доступа пользователя из бд
                    user_access_level = cm.get_user_access_level_by_user_id(user_id)

                    # Проверить уровень доступа пользователя
                    if self.recognize_user(user_access_level, access_level):
                        return await func(response, *args, **kwargs)
                    else:
                        lg.log_message(response)
                        await bot.send_message(
                            response.from_user.id,
                            text=f'Тебе сюда пока низя:(\n Мне нужно разрешение от папы...'
                        )
                else:
                    # Если нет добавить в бд с уровнем non_registered
                    self._add_user_to_unique_users(response)

            return func_restrict

        return deco_restrict

    @staticmethod
    def _add_user_to_unique_users(response):
        values = (
            response.from_user.id, # user_id
            response.from_user.username, # username
            response.from_user.first_name, # first_name
            response.from_user.last_name, # last_name
            'non_registered' # level_access
        )

        cm.add_user_to_unique_users(values)

    @staticmethod
    def get_user_access_level(user_id):
        return cm.get_user_access_level_by_user_id(user_id)

    @staticmethod
    def is_admin(message):
        user_id = message.from_user.id
        user_access_level = cm.get_user_access_level_by_user_id(user_id)
        return user_access_level in ADMIN
