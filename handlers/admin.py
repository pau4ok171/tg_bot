from authentication import AuthentificationManager


am = AuthentificationManager()


class AdminHandlers:
    """
    Класс с административными обработчиками сообщений телебота.
    """
    def __init__(self, bot_cm, menu):
        self.bot_cm = bot_cm
        self.menu = menu

    def main(self, bot):
        @bot.callback_query_handler(func=lambda call: call.data.startswith('admin'))
        @am.access_level_check(bot, access_level='admin')
        async def callback_admin_inline(call):
            # Задать язык пользователя
            self.menu.set_user_lang(call)

            """-------------------------------КАЛЕНДАРЬ-------------------------------"""
            if call.data.startswith('admin&get_read'):

                # Отправить календарь пользователю
                kb = self.menu.build_calendar_kb(self.bot_cm, call, calendar_id=1)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

                """-----------------------------АДМИН__ПАНЕЛЬ-----------------------------"""
            elif call.data.startswith('admin&panel'):
                # Отправить календарь пользователю A1
                kb = self.menu.build_admin_panel_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&user_actions'):
                # Отправить клавиатуру пользователю
                kb = self.menu.build_unique_users_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

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

            elif call.data.startswith('admin&user_management'):
                # Пагинация пользователей U
                kb, res = self.menu.build_pagin_kb(call, pagin_id=4)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

                """---------------------------УПРАВЛЕНИЕ_КНИГАМИ---------------------------"""
            elif call.data.startswith('admin&book_management&'):
                # Отправить календарь пользователю
                kb = self.menu.build_book_management_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&book_management_back&'):
                # Отправить календарь пользователю
                kb = self.menu.build_book_management_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

                """------------------------УПРАВЛЕНИЕ_ПОЛЬЗОВАТЕЛМИ------------------------"""
            elif call.data.startswith('admin&user_management_back&'):
                # Delete state
                await self.bot_cm.delete_state(call, state_id=4)

                # Пагинация пользователей U
                kb, res = self.menu.build_pagin_kb(call, pagin_id=4)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&change_user_access_level&'):
                # Создать две кнопки отличные от текущего уровня доступа
                kb = await self.menu.build_change_user_access_level_kb(call, self.bot_cm, state_id=4)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&set_access_level_non_registered&'):
                access_level = 'non_registered'
                # Создать меню подтверждения
                kb = await self.menu.build_access_level_confirmation_kb(call, self.bot_cm, access_level, state_id=4)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&set_access_level_registered&'):
                access_level = 'registered'
                # Создать меню подтверждения
                kb = await self.menu.build_access_level_confirmation_kb(call, self.bot_cm, access_level, state_id=4)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&set_access_level_admin&'):
                access_level = 'admin'
                # Создать меню подтверждения
                kb = await self.menu.build_access_level_confirmation_kb(call, self.bot_cm, access_level, state_id=4)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&set_access_level_cancel&'):
                # Получить id из базы
                user_id = await self.bot_cm.get_user_id(call, state_id=4)

                kb = await self.menu.build_user_card_kb(call, self.bot_cm, user_id, state_id=4)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&set_access_level_home&'):
                # Delete state
                await self.bot_cm.delete_state(call, state_id=4)

                # Вывести стартовую клавиатуру
                kb = self.menu.build_start_menu_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&set_access_level_confirm&'):
                # Обработать подтверждение A2
                kb = await self.menu.build_access_level_confirm_kb(call, self.bot_cm, state_id=4)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('admin&set_access_level_decline&'):
                # Удалить уровень доступа из state
                await self.bot_cm.set_access_level(call, access_level=None, state_id=4)

                # Вернуться к выбору уровня доступа.
                # Создать две кнопки отличные от текущего уровня доступа
                kb = await self.menu.build_change_user_access_level_kb(call, self.bot_cm, state_id=4)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)
