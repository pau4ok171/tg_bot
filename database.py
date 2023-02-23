from mysql.connector import connect
import config
import pandas as pd

CONFIG = config.config


class DatabaseManager:
    def crud_data(self, query: str, values: tuple =None, resp_type: str =None):
        cursor = self._execute_query(query, values)
        return self._process_cursor(cursor, resp_type)

    @staticmethod
    def _execute_query(query: str, values:  tuple = None):
        with connect(**CONFIG) as connection:
            with connection.cursor(buffered=True) as cursor:
                cursor.execute(query, values or [])
                connection.commit()
                return cursor

    def _process_cursor(self, cursor, resp_type):

        if resp_type == 'str':
            return self._build_str_response(cursor.fetchall())

        elif resp_type == 'table':
            titles = [column[0].title() for column in cursor.description]
            return self._build_table_response(cursor, titles)

        elif resp_type == 'rows':
            return cursor.fetchall()

        elif resp_type == 'dict':
            titles = [column[0].title() for column in cursor.description]
            return self._build_dict_response(titles, cursor)

        else:
            return cursor

    @staticmethod
    def _build_str_response(rows):
        prepared_res = '\n'.join(
            f"{' '.join([str(el) for el in row])}" for row in rows
        )
        return prepared_res

    @staticmethod
    def _build_table_response(rows, columns):
        df = pd.DataFrame(data=rows, columns=columns)

        prepared_table = f'<pre>{df.to_string(columns=columns, index=False)}</pre>'

        return prepared_table

    @staticmethod
    def _build_dict_response(titles, rows) -> list[dict]:
        titles = [title.lower() for title in titles]
        df = pd.DataFrame(data=rows, columns=titles)
        return df.to_dict(orient='records')




