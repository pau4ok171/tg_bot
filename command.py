import pandas as pd
import config
from queries import queries
from database import DatabaseManager


db = DatabaseManager()


WB_FULL_NAME = config.wb_full_name
TABLE_NAME = config.table_name
COL_EXCEL_LIST = config.col_excel_list
AVAILABLE_LANGUAGUES = config.available_languagues

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class CommandManager:
    @staticmethod
    def add_log_message(values):
        query = queries['add_log_message']
        db.crud_data(query, tuple(values))

    def export_data(self):
        df = self._get_df()
        query = queries['add_data']
        for values in df.values:
            db.crud_data(query, tuple(values))
        print('Данные успешно добавлены!')

    def select_count_read_books(self):
        select = ('COUNT(*) AS count',)
        where = {'YEAR(finished)': '> 1900'}
        query = self._get_select_query(select=select, where=where)
        response = db.crud_data(query, resp_type='str')
        return response

    def select_read_by_category(self):
        select = ('genre', 'COUNT(*) AS count')
        where = {'YEAR(finished)': '> 1900'}
        group_by = ('genre',)
        order_by = {'count': 'DESC'}
        query = self._get_select_query(select=select, where=where, group_by=group_by, order_by=order_by)
        response = db.crud_data(query, resp_type='table')
        return response

    def select_books(self):
        select = ('COUNT(*) AS count',)
        query = self._get_select_query(select=select)
        response = db.crud_data(query, resp_type='str')
        return response

    def select_books_by_category(self):
        select = ('genre', 'COUNT(*) AS count')
        group_by = ('genre',)
        order_by = {'count': 'DESC'}
        query = self._get_select_query(select=select, group_by=group_by, order_by=order_by)
        response = db.crud_data(query, resp_type='table')
        return response

    @staticmethod
    def select_average_data_by_category():
        query = queries['select_average_data_by_category']
        response = db.crud_data(query, resp_type='table')
        return response

    def select_books_by_language(self):
        select = ('language', 'COUNT(*) AS count')
        group_by = ('language',)
        order_by = {'count': 'DESC'}
        query = self._get_select_query(select=select, group_by=group_by, order_by=order_by)
        response = db.crud_data(query, resp_type='table')
        return response

    def select_read_by_language(self):
        select = ('language', 'COUNT(*) AS count')
        where = {'YEAR(finished)': '> 1900'}
        group_by = ('language',)
        order_by = {'count': 'DESC'}
        query = self._get_select_query(select=select, where=where, group_by=group_by, order_by=order_by)
        response = db.crud_data(query, resp_type='table')
        return response

    def select_books_by_category_and_language(self):
        select = ("COALESCE(NULLIF(genre, ''), 'TOTAL') AS genre",
                  "COALESCE(NULLIF(language, ''), 'TOTAL') AS language",
                  "COUNT(*) AS number")
        group_by = ('genre', 'language WITH ROLLUP')
        order_by = {'genre': 'ASC', 'number': 'DESC'}
        query = self._get_select_query(select=select, group_by=group_by, order_by=order_by)
        response = db.crud_data(query, resp_type='table')
        return response

    @staticmethod
    def select_top_books():
        query = queries['select_top_books']
        response = db.crud_data(query, resp_type='table')
        return response

    def select_reading_books(self):
        select = ('id', 'name')
        where = {'YEAR(started)': '> 1900', 'YEAR(finished)': '<= 1900'}
        query = self._get_select_query(select=select, where=where)
        response = db.crud_data(query, resp_type='list[tuple]')
        return response

    def select_admin_unique_users(self):
        select = ('user_id', 'username', 'MAX(added) as last_request')
        from_ = 'users'
        group_by = ('user_id', 'username')
        order_by = {'last_request': 'ASC'}
        query = self._get_select_query(
                select=select,
                from_=from_,
                group_by=group_by,
                order_by=order_by)

        response = db.crud_data(query, resp_type='table')
        return response

    def select_started_by_id(self, book_id):
        select = ('started',)
        where = {'id': f'={book_id}'}
        query = self._get_select_query(
            select=select,
            where=where
        )

        response = db.crud_data(query, resp_type='date')[0][0]

        return response

    def select_book_name_by_id(self, book_id):
        select = ('name',)
        where = {'id': f'={book_id}'}
        query = self._get_select_query(
            select=select,
            where=where
        )
        response = db.crud_data(query, resp_type='str')
        return response

    def select_token_params(self, lang):
        select = ('handler', 'name', 'buttons.id', 'trans.lang_ru', f'trans.lang_{lang}')
        from_ = 'buttons'
        join = {'translations AS trans': 'ON trans.id = translation_id'}
        where = {'buttons.id': '=%s'}
        query = self._get_select_query(
            select=select,
            from_=from_,
            join=join,
            where=where
        )
        return query

    def select_translation_by_id(self, trans_id: list, lang) -> dict:
        # Проверить доступен ли язык
        lang = lang if lang in AVAILABLE_LANGUAGUES else 'ru'
        lang = f'lang_{lang}'
        trans = {}

        # Построить query
        select = (lang,)
        from_ = 'translations'
        for tr_id in trans_id:
            where = {'id': f'={tr_id}'}
            query = self._get_select_query(
                select=select,
                from_=from_,
                where=where
            )
            response = db.crud_data(query, resp_type='str')
            trans[tr_id] = response

        return trans

    @staticmethod
    def select_books_for_pagination(values):
        query = queries['select_books_for_pagination']
        response = db.crud_data(query, values)
        return response

    @staticmethod
    def select_books_nb_non_read():
        query = queries['select_books_nb_non_read']
        response = db.crud_data(query, resp_type='str')
        return response

    @staticmethod
    def get_read(values: tuple):
        query = queries['get_read']
        db.crud_data(query, values)

    @staticmethod
    def get_started(values: tuple):
        query = queries['get_started']
        db.crud_data(query, values)

    @staticmethod
    def _get_df():
        with pd.ExcelFile(WB_FULL_NAME) as xl:
            df = xl.parse('Livres')
            prepared_df = df[COL_EXCEL_LIST]
            return prepared_df

    @staticmethod
    def _get_select_query(
             select: tuple = ('*',),
             from_: str = TABLE_NAME,
             join: dict = None,
             where: dict = None,
             group_by: tuple = None,
             order_by: dict =None
    ) -> str:

        query = f'\tSELECT {", ".join(select)}\n\tFROM {from_}'

        if join:
            query += f'\n\tJOIN {", ".join([f"{key} {value}" for key, value in join.items()])}'

        if where:
            where_str = " AND\n\t\t".join([f"{key} {value}" for key, value in where.items()])
            query += f'\n\tWHERE \n\t\t{where_str}'

        if group_by:
            query += f'\n\tGROUP BY {", ".join(group_by)}'

        if order_by:
            query += f'\n\tORDER BY {", ".join([f"{key} {value}" for key, value in order_by.items()])}'

        return query

    @staticmethod
    def get_execute_query(values=None):
        query = queries['']
        db.crud_data(query, values)


