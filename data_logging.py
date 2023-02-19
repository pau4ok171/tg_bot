import config
import inspect
from commands import CommandManager

ADMINS = config.admins
REGISTERED = config.registered
ALLOWED_ID = config.allowed_id

cm = CommandManager()

class LoggingManager:
    def __init__(self, logger=None):
        self.logger = logger

    def log_message(self, message):
        data = self._build_dict(message)
        values = data.values()
        cm.add_log_message(values)

    def print_log_info(self, message):
        self.logger.info(
            f'{inspect.getframeinfo(inspect.currentframe()).function} | '
            f'id: {message.chat.id} | '
            f'username: {message.chat.username} | '
            f'access_level: {self._get_access_level(message.chat.id)}'
        )

    def _build_dict(self, message):
        from_user = message.from_user
        user_id = from_user.id
        access_level = self._get_access_level(user_id)

        try:
            chat_id = message.chat.id
            chat_type = message.chat.type
            message_id = message.message_id
            message_content_type =message.content_type
            message_text = message.text
        except Exception as ex:
            print(ex)
            chat_id = message.json['message']['chat']['id']
            chat_type = message.json['message']['chat']['type']
            message_id = message.message.message_id
            message_content_type = message.message.content_type
            message_text = message.message.text

        data = {
            'user_id': user_id,
            'access_level': access_level,
            'username': from_user.username,
            'first_name': from_user.first_name,
            'language_code': from_user.language_code,
            'chat_id': chat_id,
            'chat_type': chat_type,
            'message_id': message_id,
            'content_type': message_content_type,
            'text': message_text
        }

        return data

    @staticmethod
    def _get_access_level(user_id):
        if user_id in REGISTERED:
            return 'registered'

        elif user_id in ADMINS:
            return 'admin'

        else:
            return 'non_registered'


