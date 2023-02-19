from private_access import private_access


class ClientHandlers:
    """
    Класс с клиентскими обработчиками сообщений телебота.
    """
    def __init__(self, lg, bot_cm, menu):
        self.lg = lg
        self.bot_cm = bot_cm
        self.menu = menu

    def main(self, bot):
        @bot.message_handler(commands=['start'])
        @private_access(bot)
        async def start_message(message):
            # Задать язык пользователя
            self.menu.set_user_lang(message)

            # Добавить запись о пользователе в бд
            self.lg.log_message(message)

            # Вывести лог в терминал
            self.lg.print_log_info(message)

            # Задать меню базовых команд
            await self.bot_cm.set_menu_commands()

            # Отправить сообщение пользователю
            kb = self.menu.build_start_menu_kb(message)
            await self.bot_cm.send_message(message, kb.text, kb.reply_markup)

        @bot.message_handler(commands=['help', 'info'])
        async def send_info(message):
            # Задать язык пользователя
            self.menu.set_user_lang(message)

            # Добавить запись о пользователе в бд
            self.lg.log_message(message)

            # Отправить текст пользователю
            text = self.menu.build_info_text(message)
            await self.bot_cm.send_message(message, text)

        @bot.message_handler(content_types=['text'])
        @private_access(bot)
        async def text_message(message):
            # Задать язык пользователя
            self.menu.set_user_lang(message)

            # Добавить запись о пользователе в бд
            self.lg.log_message(message)

            # Отправить пользователю правильную команду для начала общения с ботом
            text = self.menu.build_text_on_text_call()
            await self.bot_cm.send_message(message, text)

        @bot.callback_query_handler(func=lambda call: call.data.startswith('client'))
        @private_access(bot)
        async def callback_inline(call):
            # Задать язык пользователя
            self.menu.set_user_lang(call)

            """---------------------------ОБЩАЯ__СТАТИСТИКА---------------------------"""
            if call.data.startswith('client&common_stats'):
                # Menu_id = C1
                kb = self.menu.build_common_stats_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('client&books_nb'):
                # Отправить клавиатуру пользователю C1
                kb = self.menu.build_books_nb_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('client&read_books_nb'):
                # Отправить клавиатуру пользователю C1
                kb = self.menu.build_read_books_nb_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

                """---------------------------ПО КАТЕГОРИЯМ---------------------------"""
            elif call.data.startswith('client&stats_by_category&'):
                # Menu_id = C2
                kb = self.menu.build_stats_by_category_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('client&books_by_category&'):
                # Отправить клавиатуру пользователю C2
                kb = self.menu.build_books_by_category_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('client&read_by_category'):
                # Отправить клавиатуру пользователю C2
                kb = self.menu.build_read_by_category_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('client&average_data_by_category'):
                # Отправить клавиатуру пользователю C2
                kb = self.menu.build_average_data_by_category_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

                """---------------------------ПО ЯЗЫКАМ---------------------------"""
            elif call.data.startswith('client&stats_by_language'):
                # Отправить клавиатуру пользователю C3
                kb = self.menu.build_stats_by_language_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('client&books_by_language'):
                # Отправить клавиатуру пользователю C3
                kb = self.menu.build_books_by_language_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('client&read_by_language'):
                # Отправить клавиатуру пользователю C3
                kb = self.menu.build_read_by_language_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

                """---------------------ПО КАТЕГОРИЯМ И ЯЗЫКАМ---------------------"""
            elif call.data.startswith('client&stats_by_category_and_lang'):
                # Отправить клавиатуру пользователю C4
                kb = self.menu.build_stats_by_category_and_lang_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('client&books_by_category_and_lang'):
                # Отправить клавиатуру пользователю C4
                kb = self.menu.build_books_by_category_and_lang_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

                """---------------------------ЧТО ПОЧИТАТЬ---------------------------"""
            elif call.data.startswith('client&to_read'):
                # Отправить клавиатуру пользователю C5
                kb = self.menu.build_to_read_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

