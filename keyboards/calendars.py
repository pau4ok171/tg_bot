from builders.calendar_ import Calendar
from datetime import date, timedelta


class CalendarManager:
    def __init__(self):
        # Календарь для законченных
        self.cl_f = Calendar(
            calendar_id=1,
            max_date=date.today(),
            min_date=date.today() - timedelta(days=365),
            return_button=10001
        )

        # Календарь для начатых
        self.cl_s = Calendar(
            calendar_id=2,
            min_date=date.today() - timedelta(days=30),
            max_date=date.today() + timedelta(days=30),
            return_button=10030
        )

    def set_min_date(self, calendar_id, min_date: str):
        min_date = min_date.split('-')
        min_date = date(int(min_date[0]), int(min_date[1]), int(min_date[2]))

        if calendar_id == 1:
            self.cl_f.min_date = min_date

    def build_calendar_kb(self, response, calendar_id):
        if calendar_id == 1:
            return self.cl_f.build(response)
        elif calendar_id == 2:
            return self.cl_s.build(response)

    def process_calendar(self, call, calendar_id):
        if calendar_id == 1:
            return self.cl_f.process(call)
        elif calendar_id == 2:
            return self.cl_s.process(call)

    @staticmethod
    def func(calendar_id):
        return Calendar.func(calendar_id)