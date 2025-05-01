import asyncio
import logging

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from asker import Asker
from telegram.botsender import BotSender
from repo import TinyDbRepo
from config import get_env
from doyoubusytg.telegram.middlewares import CheckSaveUserMiddleware
from telegram.handlers import router


async def main():
    """Main entry point for the DoYouBusyTG package."""
    logging.basicConfig(level=get_env("LOG_LEVEL", "INFO").upper())
    logger = logging.getLogger(__name__)
    logger.info("Configure the logger with level %s", get_env("LOG_LEVEL", "INFO").upper())

    logger.info("Creating bot...")
    bot = Bot(token=get_env("TG_TOKEN"))
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot created.")

    logger.info("Creating repo")
    repo = TinyDbRepo(get_env("DB_NAME", "db.json"))
    logger.info("Repo created.")
    
    logger.info("Creating botsender...")
    botsender = BotSender(bot, repo)
    logger.info("Botsender created.")

    logger.info("Creating asker...")
    asker = Asker(botsender, repo)
    logger.info("Asker created.")

    logger.info("Created scheduler...")
    scheduler = AsyncIOScheduler()
    trigger = CronTrigger.from_crontab(get_env("CRON_SCHEDULE"))
    scheduler.add_job(asker, trigger)
    logger.info("Scheduler created.")
    
    logger.info("Starting scheduler...")
    scheduler.start()
    logger.info("Scheduler started.")

    logger.info("Creating dispatcher...")
    dp = Dispatcher()
    dp.message.middleware.register(CheckSaveUserMiddleware(repo))
    dp.include_router(router)
    logger.info("Dispatcher created.")

    await dp.start_polling(bot)

    logger.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
