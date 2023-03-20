import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import token

memory_storage = MemoryStorage()

bot = Bot(token)
dp = Dispatcher(bot, storage=memory_storage)
logging.basicConfig(level=logging.INFO)