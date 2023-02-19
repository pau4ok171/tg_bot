# TeleBot import
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

# Other import
import logging
import coloredlogs
import asyncio

# My import
from config import tg_token
from commands import CommandManager
from buttons import ButtonsManager
from database import DatabaseManager
from data_logging import LoggingManager
from handlers import admin, client, other
from bot_commands import TelebotCommandsManager
from keyboards import menu, calendars, paginations

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
lg = LoggingManager(logger)
db = DatabaseManager()


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

        self.bt = ButtonsManager()
        self.calendars = calendars.CalendarManager()
        self.paginations = paginations.PaginationManager()

        self.menu = menu.MenuManager(self.bt, self.calendars, self.paginations)

        self.admin = admin.AdminHandlers(self.bot_cm, self.menu)
        self.client = client.ClientHandlers(lg, self.bot_cm, self.menu)
        self.other = other.OtherHandlers(self.bot_cm, self.menu)

    def main(self):
        self.admin.main(self.bot)
        self.client.main(self.bot)
        self.other.main(self.bot)

        asyncio.run(self.bot.polling(non_stop=True))
