import asyncio
import logging

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.triggers.cron import CronTrigger
import aiohttp
import pytz

from cat_image_service import CatImageAPI
from asker_if_busy import Asker
from telegram.botsender import TelegramBotSender
from repo import TinyDbRepo
from config import get_env
from telegram.middlewares import CheckSaveUserMiddleware
from telegram.handlers import router as handlers_router
from telegram.callback import router as callback_router
from logger import IdContextFilter


async def main():
    """Main entry point for the DoYouBusyTG package."""
    filter = IdContextFilter("id")
    logging.basicConfig(level=get_env("LOG_LEVEL", "INFO").upper(),
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

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
    botsender = TelegramBotSender(bot)
    logger.info("Botsender created.")

    logger.info("Creating asker...")
    asker = Asker(botsender, repo)
    logger.info("Asker created.")

    timezone = pytz.timezone(get_env("TIMEZONE"))
    logger.info("Created scheduler...")
    scheduler = AsyncIOScheduler(executors={
        "default": AsyncIOExecutor(),
    }, timezone=timezone)
    trigger = CronTrigger.from_crontab(get_env("CRON_SCHEDULE"), timezone=timezone)
    scheduler.add_job(asker.ask, trigger)
    logger.info("Scheduler created.")

    logger.info("Starting scheduler...")
    scheduler.start()
    logger.info("Scheduler started.")

    logger.info("Creating aiohttp client...")
    async with aiohttp.ClientSession() as client:
        logger.info("Aiohttp client created.")

        logger.info("Creating cat as serivce api...")
        cat_image = CatImageAPI(get_env("CAT_API_KEY"), client)
        logger.info("Cat image service api created.")

        logger.info("Creating dispatcher...")
        dp = Dispatcher()
        dp["repo"] = repo
        dp["cat_image"] = cat_image
        dp.message.middleware.register(CheckSaveUserMiddleware(repo))
        dp.include_router(handlers_router)
        dp.include_router(callback_router)
        logger.info("Dispatcher created.")

        await dp.start_polling(bot)

        logger.info("Stop aiohttp client...")
        await client.close()
        logger.info("Aiohttp client stopped.")

        logger.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
