from builders.pagination import TelegramPagination

class PaginationManager:
    def __init__(self, bt, db, cm, bot_cm, menu):
        self.pg_f = TelegramPagination(
            bt,
            db,
            cm,
            bot_cm,
            menu,
            pagin_id=1,
            return_button=100026
        )

        self.pg_s = TelegramPagination(
            bt,
            db,
            cm,
            bot_cm,
            menu,
            pagin_id=2,
            return_button=100026
        )

        self.pg_t = TelegramPagination(
            bt,
            db,
            cm,
            bot_cm,
            menu,
            pagin_id=3,
            return_button=100026
        )

    def build_pagin_finished_reply(self, level):
        return self.pg_f.build_reply_markup(level=level)