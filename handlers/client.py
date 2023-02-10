from private_access import private_access, get_user_access_level
import inspect
from telebot import types
import config


TRANS_ID = [20, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 54, 55, 56, 57, 58]
VERSION = config.version
AVAILABLE_LANGUAGUES = config.available_languagues
ADMINS = config.admins
REGISTERED = config.registered


class ClientHandlers:
    """
    Класс с клиентскими обработчиками сообщений телебота.
    """
    def __init__(self, cm, bt, lg, cl_1, logger, pg, bot_cm):
        self.cm = cm
        self.bt = bt
        self.lg = lg
        self.cl_1 = cl_1
        self.logger = logger
        self.pg = pg
        self.bot_cm = bot_cm

    def main(self, bot):
        @bot.message_handler(commands=['start'])
        @private_access(bot)
        async def start_message(message):
            self.bt.lang = message.from_user.language_code
            trans = self.cm.select_translation_by_id(TRANS_ID, self.bt.lang)

            # Добавить запись о пользователе в бд
            self.lg.log_message(message)

            # Вывести лог в терминал
            self.logger.info(
                f'{inspect.getframeinfo(inspect.currentframe()).function} | '
                f'id: {message.chat.id} | '
                f'username: {message.chat.username} | '
                f'access_level: {get_user_access_level(message.chat.id)}'
            )

            # Меню базовых команд
            await bot.set_my_commands([
                types.BotCommand('/start', 'starter'),
                types.BotCommand('/help', 'helper'),
                types.BotCommand('info', 'informer')
            ])

            # Собрать клавиатуру
            text = f'{trans[24]}, <b>{message.chat.first_name}!</b> {trans[25]}!\n{trans[26]}'
            reply_markup = self.bt.build_start_menu(message)

            await self.bot_cm.send_message(message, text, reply_markup)

        @bot.message_handler(commands=['help', 'info'])
        async def send_info(message):
            self.bt.lang = message.from_user.language_code
            trans = self.cm.select_translation_by_id(TRANS_ID, self.bt.lang)
            user_id = message.chat.id

            # Добавить запись о пользователе в бд
            self.lg.log_message(message)

            description = trans[58]
            version = VERSION
            available_languagues = ', '.join(AVAILABLE_LANGUAGUES)
            access_level = get_user_access_level(user_id)

            text = f'<b>{trans[54]}:</b> {description}\n' \
                   f'<b>{trans[55]}:</b> {version}\n' \
                   f'<b>{trans[56]}:</b> {available_languagues}\n' \
                   f'<b>{trans[57]}:</b> {access_level}'

            # Отправить клавиатуру пользователю
            await self.bot_cm.send_message(message, text)

        @bot.message_handler(content_types=['text'])
        @private_access(bot)
        async def text_message(message):
            self.bt.lang = message.from_user.language_code
            trans = self.cm.select_translation_by_id(TRANS_ID, self.bt.lang)

            # Добавить запись о пользователе в бд
            self.lg.log_message(message)

            # Отправить пользователю правильную команду для начала общения с ботом
            await self.bot_cm.send_message(message, f'{trans[27]}')


        @bot.callback_query_handler(func=lambda call: call.data.startswith('client'))
        @private_access(bot)
        async def callback_inline(call):
            self.bt.lang = call.from_user.language_code
            trans = self.cm.select_translation_by_id(TRANS_ID, self.bt.lang)
            answer = None

            """---------------------------ОБЩАЯ__СТАТИСТИКА---------------------------"""
            if call.data.startswith('client&common_stats'):
                text = f'{trans[28]}'
                reply_markup = self.bt.build_common_stats(call)

                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith('client&books_nb'):
                # Сформировать ответ пользователю
                answer = f'{trans[29]}: '
                answer += self.cm.select_books()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                reply_markup = self.bt.build_common_stats(call)
                text = f'{trans[28]}'

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

            elif call.data.startswith('client&read_books_nb'):
                # Сформировать ответ пользователю
                answer = f'{trans[30]}: '
                answer += self.cm.select_count_read_books()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)
                # Создать новую клавиатуру
                text = f'{trans[28]}'
                reply_markup = self.bt.build_common_stats(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

                """---------------------------ПО КАТЕГОРИЯМ---------------------------"""
            elif call.data.startswith('client&stats_by_category&'):
                text = f'{trans[31]}'
                reply_markup = self.bt.build_stats_by_category(call)

                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith('client&books_by_category&'):
                # Сформировать ответ пользователю
                answer = f'{trans[32]}:\n'
                answer += self.cm.select_books_by_category()
                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)
                # Создать новую клавиатуру
                text = f'{trans[31]}'
                reply_markup = self.bt.build_stats_by_category(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

            elif call.data.startswith('client&read_by_category'):
                # Сформировать ответ пользователю
                answer = f'{trans[33]}:\n'
                answer += self.cm.select_read_by_category()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{trans[31]}'
                reply_markup = self.bt.build_stats_by_category(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

            elif call.data.startswith('client&average_data_by_category'):
                # Сформировать ответ пользователю
                answer = f'{trans[34]}м:\n'
                answer += self.cm.select_average_data_by_category()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{trans[31]}'
                reply_markup = self.bt.build_stats_by_category(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

                """---------------------------ПО ЯЗЫКАМ---------------------------"""
            elif call.data.startswith('client&stats_by_language'):
                text = f'{trans[35]}'
                reply_markup = self.bt.build_stats_by_language(call)

                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith('client&books_by_language'):
                # Сформировать ответ пользователю
                answer = f'{trans[36]}:\n'
                answer += self.cm.select_books_by_language()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{trans[35]}'
                reply_markup = self.bt.build_stats_by_language(call)


                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

            elif call.data.startswith('client&read_by_language'):
                # Сформировать ответ пользователю
                answer = f'{trans[37]}:\n'
                answer += self.cm.select_read_by_language()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{trans[35]}'
                reply_markup = self.bt.build_stats_by_language(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

                """---------------------ПО КАТЕГОРИЯМ И ЯЗЫКАМ---------------------"""
            elif call.data.startswith('client&stats_by_category_and_lang'):
                text = f'{trans[38]}'
                reply_markup = self.bt.build_stats_by_category_and_lang(call)

                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith('client&books_by_category_and_lang'):
                # Сформировать ответ пользователю
                answer = f'{trans[39]}:\n'
                answer += self.cm.select_books_by_category_and_language()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{trans[38]}'
                reply_markup = self.bt.build_stats_by_category_and_lang(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

                """---------------------------ЧТО ПОЧИТАТЬ---------------------------"""
            elif call.data.startswith('client&to_read'):
                text = f'{trans[20]}'
                reply_markup = self.bt.build_to_read(call)

                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith('client&top_books'):
                # Сформировать ответ пользователю
                answer = f'{trans[40]}:\n'
                answer += self.cm.select_top_books()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{trans[41]}'
                reply_markup = self.bt.build_to_read(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

            if answer:
                await self.bot_cm.send_message(call, answer)