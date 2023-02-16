from builders.calendar_ import Calendar
from datetime import date, timedelta


class CalendarManager:
    def __init__(self, bt):
        # Календарь для законченных
        self.cl_f = Calendar(
            bt=bt,
            calendar_id=1,
            max_date=date.today(),
            min_date=date.today() - timedelta(days=365),
            return_button=10001
        )

        # Календарь для начатых
        self.cl_s = Calendar(
            bt=bt,
            calendar_id=2,
            min_date=date.today() - timedelta(days=30),
            max_date=date.today() + timedelta(days=30),
            return_button=10030
        )

    def set_min_date_clf(self, min_date):
        self.cl_f.min_date = min_date

    def build_calendar_clf_kb(self):
        return self.cl_f.build()
