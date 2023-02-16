from private_access import private_admin_access



TRANS_ID = [20, 21, 22, 23, 48, 50, 51]


class AdminHandlers:
    """
    Класс с административными обработчиками сообщений телебота.
    """
    def __init__(self, cm, bt, lg, pg, bot_cm, menu, calendars):
        self.cm = cm
        self.bt = bt
        self.lg = lg
        self.pg = pg
        self.bot_cm = bot_cm
        self.menu = menu
        self.calendars = calendars

    def main(self, bot):
        @bot.callback_query_handler(func=lambda call: call.data.startswith('admin'))
        @private_admin_access(bot)
        async def callback_admin_inline(call):
            # Задать язык пользователя
            self.menu.set_user_lang(call)

            """-------------------------------КАЛЕНДАРЬ-------------------------------"""
            if call.data.startswith('admin&get_read'):
                # Отправить календарь пользователю
                kb = self.menu.build_calendar_clf_rb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&book_management'):
                # Отправить календарь пользователю
                kb = self.menu.build_book_management_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

                """-----------------------------АДМИН__ПАНЕЛЬ-----------------------------"""
            elif call.data.startswith('admin&panel'):
                # Отправить календарь пользователю
                kb = self.menu.build_admin_panel_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&unique_users'):
                # Сформировать ответ пользователю TODO
                answer = self.cm.select_admin_unique_users()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                reply_markup = self.bt.build_admin_panel(call)
                text = f'{trans[23]}'

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

                """-------------------------------ПАГИНАЦИЯ-------------------------------"""
            elif call.data.startswith('admin&mark_started&'):
                # Отметить прочитанной
                kb = self.menu.build_pagin_finished_kb()
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&mark_read'):
                # Отметить начатой
                # Вывести список начатых книг кнопкой TODO
                reply_markup = self.bt.build_get_books_read(call)
                text = f'{trans[22]}'
                await self.bot_cm.edit_message(call, text, reply_markup)