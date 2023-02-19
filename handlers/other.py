from private_access import private_access


class OtherHandlers:
    """
    Класс с дополнительными обработчиками сообщений телебота.
    """
    def __init__(self, bot_cm, menu):

        self.bot_cm = bot_cm
        self.menu = menu

    def main(self, bot):
        # Календарь для законченных книг
        @bot.callback_query_handler(func=self.menu.cal_func(calendar_id=1))
        async def calender_for_finished(call):
            # Задать язык пользователя
            self.menu.set_user_lang(call)

            kb, res = self.menu.process_calendar_kb(call, calendar_id=1)

            if res:
                kb = await self.menu.process_calendar_result(
                    self.bot_cm,
                    res,
                    calendar_id=1,
                    call=call
                )

            await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

        # Календарь для начатых книг
        @bot.callback_query_handler(func=self.menu.cal_func(calendar_id=2))
        async def calender_for_started(call):
            # Задать язык пользователя
            self.menu.set_user_lang(call)

            kb, res = self.menu.process_calendar_kb(call, calendar_id=2)

            if res:
                kb = await self.menu.process_calendar_result(
                    self.bot_cm,
                    res,
                    calendar_id=2,
                    call=call
                )

            await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

        @bot.callback_query_handler(func=self.menu.pag_func(pagin_id=1))
        @private_access(bot)
        async def pagination(call):
            # Задать язык пользователя
            self.menu.set_user_lang(call)

            # Сформировать пагинацию и отправить пользователю
            kb, res = self.menu.process_pagin_kb(pagin_id=1, call=call)
            if kb:
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)
            elif res:
                # Отправить календарь пользователю
                kb = await self.menu.build_calendar_kb(self.bot_cm, call, book_id=res, calendar_id=1)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

        @bot.callback_query_handler(func=self.menu.pag_func(pagin_id=2))
        @private_access(bot)
        async def pagination(call):
            # Задать язык пользователя
            self.menu.set_user_lang(call)

            # Сформировать пагинацию и отправить пользователю
            kb, res = self.menu.process_pagin_kb(pagin_id=2, call=call)
            if kb:
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)
            elif res:
                # Отправить календарь пользователю
                kb = await self.menu.build_calendar_kb(self.bot_cm, call, book_id=res, calendar_id=2)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

        @bot.callback_query_handler(func=self.menu.pag_func(pagin_id=3))
        @private_access(bot)
        async def pagination(call):
            # Задать язык пользователя
            self.menu.set_user_lang(call)

            # Сформировать пагинацию и отправить пользователю
            kb, res = self.menu.process_pagin_kb(pagin_id=3, call=call)
            if kb:
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)
            elif res:
                # Обработать полученный объект
                print(res)

        @bot.callback_query_handler(func=lambda call: True)
        @private_access(bot)
        async def callback_inline(call):
            # Задать язык пользователя
            self.menu.set_user_lang(call)

            if call.data.startswith('other&calendar_1_cancel'):
                # К книгам finished
                await bot.delete_state(call.message.from_user.id, call.message.id)

                kb, res = self.menu.build_calendar_cancel_kb(call, pagin_id=1)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('other&calendar_2_cancel'):
                # К книгам started
                await bot.delete_state(call.message.from_user.id, call.message.id)

                kb, res = self.menu.build_calendar_cancel_kb(call, pagin_id=2)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('other&calendar_home'):
                # Отчистить сохраненные состояния в памяти
                await bot.delete_state(call.message.from_user.id, call.message.id)

                kb = self.menu.build_start_menu_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith(('other&home_as_back&', 'other&home_as_home&')):
                kb = self.menu.build_start_menu_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            # Обновить информацию о книге
            elif call.data.startswith('other&confirm_get_finished_book'):
                kb = await self.menu.process_confirm_crud_book(self.bot_cm, call, calendar_id=1)

                # Отчистить сохраненные состояния в памяти
                await bot.delete_state(call.message.from_user.id, call.message.id)

                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            # Обновить информацию о книге
            elif call.data.startswith('other&confirm_get_started_book'):
                kb = await self.menu.process_confirm_crud_book(self.bot_cm, call, calendar_id=2)

                # Отчистить сохраненные состояния в памяти
                await bot.delete_state(call.message.from_user.id, call.message.id)

                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('other&decline_get_finished_book'):
                # Отчистить сохраненные состояния в памяти
                async with bot.retrieve_data(call.message.from_user.id,
                                       call.message.chat.id) as data:
                    data['finished'] = None
                    book_id = data['book_id']

                # Отправить календарь пользователю
                kb = await self.menu.build_calendar_kb(self.bot_cm, call, book_id, calendar_id=1)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

            elif call.data.startswith('other&decline_get_started_book&'):
                # Удалить состояние
                async with bot.retrieve_data(call.message.from_user.id,
                                       call.message.chat.id) as data:
                    data['started'] = None
                    book_id = data['book_id']

                # Отправить календарь пользователю
                kb = await self.menu.build_calendar_kb(self.bot_cm, call, book_id, calendar_id=2)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)



