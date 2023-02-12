from telebot import types
import config
from private_access import get_user_access_level

VERSION = config.version
AVAILABLE_LANGUAGUES = config.available_languagues
from keyboards.keyboard import Keyboard

class MenuManager(Keyboard):
    def __init__(self, bot, bt, db, cm, bot_cm):
        # Инициализация родительского класса
        super().__init__(bot, bt, db, cm, bot_cm)

    async def set_menu_commands(self):
        """
        Задать базовые команды для тг бота
        """
        await self.bot.set_my_commands([
            types.BotCommand('/start', 'starter'),
            types.BotCommand('/help', 'helper'),
            types.BotCommand('info', 'informer')
        ])

    def build_start_menu_kb(self, response):
        text = f'{self.trans[24]}, <b>{response.from_user.first_name}!</b> {self.trans[25]}!\n{self.trans[26]}'
        reply_markup = self.bt.build_start_menu(response)
        return self._build_keyboard(text, reply_markup)

    def build_common_stats_kb(self, response):
        text = f'{self.trans[28]}'
        reply_markup = self.bt.build_common_stats(response)
        return self._build_keyboard(text, reply_markup)

    def build_info_text(self, response):
        user_id = response.from_user.id
        description = self.trans[58]
        version = VERSION
        available_languagues = ', '.join(AVAILABLE_LANGUAGUES)
        access_level = get_user_access_level(user_id)

        text = f'<b>{self.trans[54]}:</b> {description}\n' \
               f'<b>{self.trans[55]}:</b> {version}\n' \
               f'<b>{self.trans[56]}:</b> {available_languagues}\n' \
               f'<b>{self.trans[57]}:</b> {access_level}'

        return text

    # Текст для ответа на текстовое сообщение пользователя
    def build_text_on_text_call(self):
        text = f'{self.trans[27]}'

        return text



