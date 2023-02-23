from builders.pagination import TelegramPagination
from schemas import Keyboard

class PaginationManager:
    def __init__(self):
        self.pg_f = TelegramPagination(
            pagin_id=1,
            return_button=10024
        )

        self.pg_s = TelegramPagination(
            pagin_id=2,
            return_button=10024
        )

        self.pg_t = TelegramPagination(
            pagin_id=3,
            return_button=10024
        )

        self.pg_u = TelegramPagination(
            pagin_id=4,
            return_button=10031
        )

    def build_pagin_kb(self, call, pagin_id: int) -> tuple[Keyboard | None, int | None]:
        if pagin_id == 1:
            return self.pg_f.build(call)
        elif pagin_id == 2:
            return self.pg_s.build(call)
        elif pagin_id == 3:
            return self.pg_t.build(call)
        elif pagin_id == 4:
            return self.pg_u.build(call)

    def get_transaction_last_page(self, pagin_id: int) ->int:
        if pagin_id == 1:
            return self.pg_f.transaction_last_page
        elif pagin_id == 2:
            return self.pg_s.transaction_last_page
        elif pagin_id == 3:
            return self.pg_t.transaction_last_page
        elif pagin_id == 4:
            return self.pg_u.transaction_last_page

    def process_pagin_kb(self, pagin_id: int, call) -> tuple[Keyboard | None, int | None]:
        if pagin_id == 1:
            return self.pg_f.process(call)
        elif pagin_id == 2:
            return self.pg_s.process(call)
        elif pagin_id == 3:
            return self.pg_t.process(call)
        elif pagin_id == 4:
            return self.pg_u.process(call)

    @staticmethod
    def func(pagin_id: int) -> bool:
        return TelegramPagination.func(pagin_id)