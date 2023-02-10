from private_access import private_admin_access
from handlers.states import States
import math

TRANS_ID = [21, 22, 23, 48, 50, 51]


class AdminHandlers:
    """
    Класс с административными обработчиками сообщений телебота.
    """
    def __init__(self, cm, bt, lg, cl_1, pg, bot_cm):
        self.cm = cm
        self.bt = bt
        self.lg = lg
        self.cl_1 = cl_1
        self.pg = pg
        self.bot_cm = bot_cm

    def main(self, bot):
        @bot.callback_query_handler(func=lambda call: call.data.startswith('admin'))
        @private_admin_access(bot)
        async def callback_admin_inline(call):
            self.bt.lang = call.from_user.language_code
            trans = self.cm.select_translation_by_id(TRANS_ID, self.bt.lang)
            answer = None
            """-------------------------------КАЛЕНДАРЬ-------------------------------"""
            if call.data.startswith('admin&get_read'):

                params = self.bt.process_callback_data(call)

                # Найти id книги в полученной data
                book_id = params['data']['id']

                # Отчистить сохраненные состояния в памяти
                await bot.delete_state(call.message.from_user.id, call.message.id)

                # Открыть состояние id книги
                await bot.set_state(call.message.from_user.id,
                                    States.book_id,
                                    call.message.chat.id)

                # Удалить клавиатуру
                self.cl_1._keyboard = None
                self.cl_1.locale = call.from_user.language_code

                # Сохранить состояние id книги в память
                async with bot.retrieve_data(call.message.from_user.id, call.message.chat.id) as data:
                    data['book_id'] = book_id
                    self.cl_1.min_date = self.cm.select_started_by_id(data['book_id'])

                # Добавить дополнительные кнопки в календарь
                self.cl_1.additional_buttons = self.bt.additional_buttons_for_get_read('finished')
                # Построить календарь
                reply_markup, step = self.cl_1.build()

                # Отправить календарь пользователю
                text = f'{trans[21]}'
                await self.bot_cm.edit_message(call=call, text=text, reply_markup=reply_markup)

            elif call.data.startswith('admin&book_management'):
                reply_markup = self.bt.build_books_management(call)
                text = f'{trans[48]}'
                await self.bot_cm.edit_message(call=call, text=text, reply_markup=reply_markup)

            elif call.data.startswith('admin&mark_read'):
                # Вывести список начатых книг кнопкой
                reply_markup = self.bt.build_get_books_read()
                text = f'{trans[22]}'
                await self.bot_cm.edit_message(call=call, text=text, reply_markup=reply_markup)

                """-----------------------------АДМИН__ПАНЕЛЬ-----------------------------"""
            elif call.data.startswith('admin&panel'):
                reply_markup = self.bt.build_admin_panel(call)
                text = f'{trans[23]}'
                await self.bot_cm.edit_message(call=call, text=text, reply_markup=reply_markup)

            elif call.data.startswith('admin&unique_users'):
                # Сформировать ответ пользователю
                answer = self.cm.select_admin_unique_users()

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                reply_markup = self.bt.build_admin_panel(call)
                text = f'{trans[23]}'
                # Отправить клавиатуру пользователю
                await bot.send_message(call.from_user.id, text, reply_markup=reply_markup)

                """-------------------------------ПАГИНАЦИЯ-------------------------------"""
            elif call.data.startswith('admin&mark_started&'):

                reply_markup = self.pg.build_reply_markup(level=1)
                last_page = math.ceil(int(self.cm.select_books_nb_non_read()) / 10)
                text = f'{trans[50]} 1 {trans[51]} {last_page}'
                await self.bot_cm.edit_message(call=call, text=text, reply_markup=reply_markup)


            if answer:
                await bot.send_message(call.message.chat.id, answer)