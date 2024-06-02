from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.mongo import MongoStorage
from motor.motor_asyncio import AsyncIOMotorClient
from bot import config

from bot import config

bot = Bot(
    token=config.BOT_TOKEN,
    parse_mode=types.ParseMode.HTML,
)

client = AsyncIOMotorClient(config.MONGO_URL)
storage = MongoStorage(client=client, db_name='aiogram_fsm', collection_name='states_and_data')

dp = Dispatcher(
    bot=bot,
    storage=storage,
)

__all__ = (
    "bot",
    "storage",
    "dp",
)
