from private_access import private_access
from builders.calendar_ import Calendar
from handlers.states import States
from datetime import date
import math
from telegram_bot_calendar.static import LSTEP_text

TRANS_ID = [42, 43, 44, 45, 46, 20, 21, 22, 26, 50, 51, 52]


class OtherHandlers:
    """
    Класс с дополнительными обработчиками сообщений телебота.
    """
    def __init__(self, cm, bt, lg, pg, bot_cm, menu):
        self.cm = cm
        self.bt = bt
        self.lg = lg
        self.pg = pg
        self.bot_cm = bot_cm
        self.menu = menu

    def main(self, bot):
        # Календарь для законченных книг
        @bot.callback_query_handler(func=Calendar.func(calendar_id=1))
        async def calender_for_finished(call):
            lang = call.from_user.language_code
            self.bt.lang = lang
            trans = self.cm.select_translation_by_id(TRANS_ID, lang)

            result, key, step = self.cl_1.process(call.data)
            if not result and key:
                text = f'{trans[42]} {LSTEP_text[lang][step]}'
                reply_markup = key
                await self.bot_cm.edit_message(call, text, reply_markup)

            elif result:
                # Открыть состояние id книги
                await bot.set_state(call.message.from_user.id,
                                    States.book_id,
                                    call.message.chat.id)

                # Сохранить состояние finished в память
                # и сформировать кортеж для отправки в бд
                async with bot.retrieve_data(call.message.from_user.id,
                                       call.message.chat.id) as data:
                    data['finished'] = result
                    values = (data['finished'], int(data['book_id']))

                book_name = self.cm.select_book_name_by_id(values[1])
                read_date = date.strftime(values[0], '%d-%m-%Y')

                # Запросить у пользователя подтверждение для внесения изменения в бд
                text = f'<b>{trans[43]}:</b> {book_name}\n' \
                       f'<b>{trans[44]}:</b> {read_date}\n' \
                       f'<b>{trans[45]}</b>'

                reply_markup = self.bt.build_confirm_adding('finished', call)
                await self.bot_cm.edit_message(call, text, reply_markup)

        # Календарь для начатых книг
        @bot.callback_query_handler(func=Calendar.func(calendar_id=2))
        async def calender_for_started(call):
            self.bt.lang = call.from_user.language_code
            trans = self.cm.select_translation_by_id(TRANS_ID, self.bt.lang)
            lang = call.from_user.language_code

            result, key, step = self.cl_2.process(call.data)
            if not result and key:
                text = f'{trans[42]} {LSTEP_text[lang][step]}'
                reply_markup = key
                await self.bot_cm.edit_message(call, text, reply_markup)

            elif result:
                # Открыть состояние id книги
                await bot.set_state(call.message.from_user.id,
                                    States.book_id,
                                    call.message.chat.id)

                # Сохранить состояние started в память
                # и сформировать кортеж для отправки в бд
                async with bot.retrieve_data(call.message.from_user.id,
                                             call.message.chat.id) as data:
                    data['started'] = result
                    values = (data['started'], int(data['book_id']))

                book_name = self.cm.select_book_name_by_id(values[1])
                start_date = date.strftime(values[0], '%d-%m-%Y')

                # Запросить у пользователя подтверждение для внесения изменения в бд
                text = f'<b>{trans[43]}:</b> {book_name}\n' \
                       f'<b>{trans[52]}:</b> {start_date}\n' \
                       f'<b>{trans[45]}</b>'

                reply_markup = self.bt.build_confirm_adding('started', call)
                await self.bot_cm.edit_message(call, text, reply_markup)

        @bot.callback_query_handler(func=self.pg.func())
        @private_access(bot)
        async def pagination(call):
            # Сформировать пагинацию и отправить пользователю
            await self.pg.process(bot, call)

        @bot.callback_query_handler(func=self.cl_test.func())
        @private_access(bot)
        async def calendar_test(call):
            # Задать язык пользователя
            self.menu.set_user_lang(call)
            self.cl_test.set_user_lang(call)
            print(call.data)
            # Сформировать календарь и отправить пользователю
            kb, chosen_date = self.cl_test.process(call)
            if kb:
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)
            elif chosen_date:
                kb = self.menu.build_start_menu_kb(call)
                await self.bot_cm.edit_message(call, kb.text, kb.reply_markup)

                await self.bot_cm.send_message(call, f'Выбрана дата: {chosen_date}')


        @bot.callback_query_handler(func=lambda call: True)
        @private_access(bot)
        async def callback_inline(call):
            self.bt.lang = call.from_user.language_code
            trans = self.cm.select_translation_by_id(TRANS_ID, self.bt.lang)

            if call.data.startswith('other&calendar_1_cancel'):
                await bot.delete_state(call.message.from_user.id, call.message.id)

                text = f'{trans[22]}'
                reply_markup = self.bt.build_get_books_read(call)

                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data == 'other&calendar_2_cancel':
                await bot.delete_state(call.message.from_user.id, call.message.id)
                last_page = math.ceil(int(self.cm.select_books_nb_non_read()) / 10)

                text = f'{trans[50]} 1 {trans[51]} {last_page}'
                reply_markup = self.pg.build_reply_markup(level=1)

                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith('other&calendar_home'):

                await bot.delete_state(call.message.from_user.id, call.message.id)

                text = f'{trans[20]}'
                reply_markup = self.bt.build_start_menu(call)
                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith(('other&home_as_back&', 'other&home_as_home&')):
                text = f'{trans[20]}'
                reply_markup = self.bt.build_start_menu(call)

                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith('other&confirm_get_finished_book'):
                # Открыть менеджер состояния и извлечь данные в кортеж
                async with bot.retrieve_data(call.message.from_user.id,
                                       call.message.chat.id) as data:
                    values = (data['finished'], int(data['book_id']))

                # Отправить команду на добавление данных в бд
                self.cm.get_read(values)

                # Отчистить сохраненные состояния в памяти
                await bot.delete_state(call.message.from_user.id, call.message.id)

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{trans[26]}'
                reply_markup = self.bt.build_start_menu(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.edit_message(call, text, reply_markup)

                # Отправить сообщение об успешном завершении операции
                await self.bot_cm.send_message(call, f'{trans[46]}!')

            elif call.data.startswith('other&decline_get_finished_book'):
                # Удалить состояние
                async with bot.retrieve_data(call.message.from_user.id,
                                       call.message.chat.id) as data:
                    data['finished'] = None

                # Добавить дополнительные кнопки в календарь
                self.cl_1.additional_buttons = self.bt.additional_buttons_for_get_read('finished')
                # Построить календарь
                text = f'{trans[21]}'
                reply_markup, step = self.cl_1.build(call)

                # Отправить календарь пользователю
                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith('other&decline_get_started_book&'):
                # Удалить состояние
                async with bot.retrieve_data(call.message.from_user.id,
                                       call.message.chat.id) as data:
                    data['started'] = None

                # Добавить дополнительные кнопки в календарь
                self.cl_1.additional_buttons = self.bt.additional_buttons_for_get_read('started')

                # Построить календарь
                text = f'{trans[21]}'
                reply_markup, step = self.cl_2.build()

                # Отправить календарь пользователю
                await self.bot_cm.edit_message(call, text, reply_markup)

            elif call.data.startswith('other&confirm_get_started_book'):
                # Открыть менеджер состояния и извлечь данные в кортеж
                async with bot.retrieve_data(call.message.from_user.id,
                                       call.message.chat.id) as data:
                    values = (data['started'], int(data['book_id']))

                # Отправить команду на добавление данных в бд
                self.cm.get_started(values)

                # Отчистить сохраненные состояния в памяти
                await bot.delete_state(call.message.from_user.id, call.message.id)

                # Удалить клавиатуру
                await bot.delete_message(call.from_user.id, call.message.id)

                # Создать новую клавиатуру
                text = f'{trans[26]}'
                reply_markup = self.bt.build_start_menu(call)

                # Отправить клавиатуру пользователю
                await self.bot_cm.send_message(call, text, reply_markup)

                # Отправить сообщение об успешном завершении операции
                await self.bot_cm.send_message(call, f'{trans[46]}!')
