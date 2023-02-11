from private_access import private_access


class ClientHandlers:
    """
    Класс с клиентскими обработчиками сообщений телебота.
    """
    def __init__(self, cm, bt, lg, bot_cm, menu):
        self.cm = cm
        self.bt = bt
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
            await self.menu.set_menu_commands()

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
            answer = None

            """---------------------------ОБЩАЯ__СТАТИСТИКА---------------------------"""
            if call.data.startswith('client&common_stats'):
                kb = self.menu.build_common_stats_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('client&books_nb'):
                # Сформировать ответ пользователю
                answer = f'{self.menu.trans[29]}: '
                answer += self.cm.select_books()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Отправить клавиатуру пользователю
                kb = self.menu.build_common_stats_kb(call)
                await self.bot_cm.send_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('client&read_books_nb'):
                # Сформировать ответ пользователю
                answer = f'{self.menu.trans[30]}: '
                answer += self.cm.select_count_read_books()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)
                # Создать новую клавиатуру
                text = f'{self.menu.trans[28]}'
                reply_markup = self.bt.build_common_stats(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

                """---------------------------ПО КАТЕГОРИЯМ---------------------------"""
            elif call.data.startswith('client&stats_by_category&'):
                text = f'{self.menu.trans[31]}'
                reply_markup = self.bt.build_stats_by_category(call)

                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith('client&books_by_category&'):
                # Сформировать ответ пользователю
                answer = f'{self.menu.trans[32]}:\n'
                answer += self.cm.select_books_by_category()
                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)
                # Создать новую клавиатуру
                text = f'{self.menu.trans[31]}'
                reply_markup = self.bt.build_stats_by_category(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

            elif call.data.startswith('client&read_by_category'):
                # Сформировать ответ пользователю
                answer = f'{self.menu.trans[33]}:\n'
                answer += self.cm.select_read_by_category()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{self.menu.trans[31]}'
                reply_markup = self.bt.build_stats_by_category(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

            elif call.data.startswith('client&average_data_by_category'):
                # Сформировать ответ пользователю
                answer = f'{self.menu.trans[34]}м:\n'
                answer += self.cm.select_average_data_by_category()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{self.menu.trans[31]}'
                reply_markup = self.bt.build_stats_by_category(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

                """---------------------------ПО ЯЗЫКАМ---------------------------"""
            elif call.data.startswith('client&stats_by_language'):
                text = f'{self.menu.trans[35]}'
                reply_markup = self.bt.build_stats_by_language(call)

                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith('client&books_by_language'):
                # Сформировать ответ пользователю
                answer = f'{self.menu.trans[36]}:\n'
                answer += self.cm.select_books_by_language()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{self.menu.trans[35]}'
                reply_markup = self.bt.build_stats_by_language(call)


                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

            elif call.data.startswith('client&read_by_language'):
                # Сформировать ответ пользователю
                answer = f'{self.menu.trans[37]}:\n'
                answer += self.cm.select_read_by_language()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{self.menu.trans[35]}'
                reply_markup = self.bt.build_stats_by_language(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

                """---------------------ПО КАТЕГОРИЯМ И ЯЗЫКАМ---------------------"""
            elif call.data.startswith('client&stats_by_category_and_lang'):
                text = f'{self.menu.trans[38]}'
                reply_markup = self.bt.build_stats_by_category_and_lang(call)

                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith('client&books_by_category_and_lang'):
                # Сформировать ответ пользователю
                answer = f'{self.menu.trans[39]}:\n'
                answer += self.cm.select_books_by_category_and_language()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{self.menu.trans[38]}'
                reply_markup = self.bt.build_stats_by_category_and_lang(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

                """---------------------------ЧТО ПОЧИТАТЬ---------------------------"""
            elif call.data.startswith('client&to_read'):
                text = f'{self.menu.trans[20]}'
                reply_markup = self.bt.build_to_read(call)

                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith('client&top_books'):
                # Сформировать ответ пользователю
                answer = f'{self.menu.trans[40]}:\n'
                answer += self.cm.select_top_books()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{self.menu.trans[41]}'
                reply_markup = self.bt.build_to_read(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

            if answer:
                await self.bot_cm.send_message(call, answer)