import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import get_env
from telegram.middleware import CheckSaveUserMiddleware
from telegram.handlers import router


logging.basicConfig(level=get_env("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger(__name__)

async def main():
    """Main entry point for the DoYouBusyTG package."""

    logger.info("Start dispatcher creating...")
    dp = Dispatcher()
    dp.message.middleware.register(CheckSaveUserMiddleware())
    dp.include_router(router)
    logger.info("Dispatcher created.")

    logger.info("Starting bot...")
    bot = Bot(token=get_env("TG_TOKEN"))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    logger.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
