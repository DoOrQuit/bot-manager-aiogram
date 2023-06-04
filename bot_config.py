import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv

# Environment variable config
load_dotenv(".env.bot")


BOT_TOKEN = os.getenv('BOT_TOKEN')


# Aiogram bot construction
storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
