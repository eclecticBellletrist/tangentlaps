import aiogram
from bot import utils, config
from bot.loader import dp

# The configuration of the modules using import
from bot import middlewares, filters, handlers


async def on_startup(dispatcher: aiogram.Dispatcher):
    """
    Действия выполняемые при старте.
    """
    await utils.setup_default_commands(dispatcher)
    await utils.notify_admins(config.SUPERUSER_IDS)


if __name__ == '__main__':
    utils.setup_logger("INFO", ["sqlalchemy.engine", "aiogram.bot.api"])
    aiogram.executor.start_polling(
        dp, on_startup=on_startup, skip_updates=config.SKIP_UPDATES
    )
