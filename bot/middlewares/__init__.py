from aiogram.contrib.middlewares.logging import LoggingMiddleware
from loguru import logger

from bot.loader import dp

if __name__ == "bot.middlewares":
    dp.middleware.setup(LoggingMiddleware())
    logger.info('Middlewares are successfully configured')
