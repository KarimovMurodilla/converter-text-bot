from googletrans import Translator

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.misc.connection import Database

from utils.misc.voice.voice_to_text import Voice2Text
from utils.misc.extract_file.extract_text import ExtractText


# AIOgram
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# DB
db = Database()


# Google Translate
translator = Translator()


# Speech recognition
v2t = Voice2Text()


# Docx, fitz
file2text = ExtractText()