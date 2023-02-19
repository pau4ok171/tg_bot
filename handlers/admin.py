from private_access import private_admin_access


class AdminHandlers:
    """
    Класс с административными обработчиками сообщений телебота.
    """
    def __init__(self, bot_cm, menu):
        self.bot_cm = bot_cm
        self.menu = menu

    def main(self, bot):
        @bot.callback_query_handler(func=lambda call: call.data.startswith('admin'))
        @private_admin_access(bot)
        async def callback_admin_inline(call):
            # Задать язык пользователя
            self.menu.set_user_lang(call)

            """-------------------------------КАЛЕНДАРЬ-------------------------------"""
            if call.data.startswith('admin&get_read'):

                # Отправить календарь пользователю
                kb = self.menu.build_calendar_kb(self.bot_cm, call, calendar_id=1)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&book_management'):
                # Отправить календарь пользователю
                kb = self.menu.build_book_management_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

                """-----------------------------АДМИН__ПАНЕЛЬ-----------------------------"""
            elif call.data.startswith('admin&panel'):
                # Отправить календарь пользователю A1
                kb = self.menu.build_admin_panel_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&unique_users'):
                # Отправить клавиатуру пользователю
                kb = self.menu.build_unique_users_kb(call)
                await self.bot_cm.send_message(call, kb.text, kb.reply_markup)

                """-------------------------------ПАГИНАЦИЯ-------------------------------"""
            elif call.data.startswith('admin&mark_read'):
                # Отметить начатой trans 22 S
                kb, res = self.menu.build_pagin_kb(call, pagin_id=1)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&mark_started&'):
                # Отметить прочитанной F
                kb, res = self.menu.build_pagin_kb(call, pagin_id=2)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&top_books'):
                # ТОП trans 40 T
                kb, res = self.menu.build_pagin_kb(call, pagin_id=3)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)