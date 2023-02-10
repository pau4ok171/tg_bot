# TeleBot import
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

# Other import
import logging
import coloredlogs
import asyncio
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import date,timedelta

# My import
from config import tg_token
from command import CommandManager
from buttons import ButtonsManager
from database import DatabaseManager
from data_logging import LoggingManager
from handlers import admin, client, other
from pagination import TelegramPagination
from tg_bot_commands import TelebotCommandsManager

# Telebot token
TG_TOKEN = tg_token

# Logging
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    filemode='a',
                    filename='tg_bot_logging.log',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)

# Classes initialisation
cm = CommandManager()
lg = LoggingManager()
db = DatabaseManager()

# Календарь для законченных
cl_1 = DetailedTelegramCalendar(
    calendar_id=1,
    locale='ru',
    max_date=date.today(),
    min_date=date.today() - timedelta(days=365)
)

# Календарь для начатых
cl_2 = DetailedTelegramCalendar(
    calendar_id=2,
    locale='ru',
    min_date=date.today() - timedelta(days=30),
    max_date=date.today() + timedelta(days=30)
)


class TelebotManager:
    """
    Класс для инициализации телебота.
    """
    def __init__(self):
        self.bot = AsyncTeleBot(
            TG_TOKEN,
            parse_mode='HTML',
            state_storage=StateMemoryStorage(),
            colorful_logs=True
        )

        self.bot_cm = TelebotCommandsManager(self.bot)
        self.bt = ButtonsManager(self.bot_cm)
        self.pg = TelegramPagination( self.bt, db, cm, cl_2, self.bot_cm)
        self.admin = admin.AdminHandlers(cm,  self.bt, lg, cl_1, self.pg, self.bot_cm)
        self.client = client.ClientHandlers(cm, self.bt, lg, cl_1, logger, self.pg, self.bot_cm)
        self.other = other.OtherHandlers(cm,  self.bt, lg, cl_1, cl_2, self.pg, self.bot_cm)


    def main(self):

        self.admin.main(self.bot)
        self.client.main(self.bot)
        self.other.main(self.bot)

        asyncio.run(self.bot.polling(non_stop=True))
