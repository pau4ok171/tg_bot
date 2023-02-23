from dataclasses import dataclass
from telebot import types

@dataclass
class Keyboard:
    text: str
    reply_markup: types.InlineKeyboardMarkup
