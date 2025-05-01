from logging import getLogger, Logger

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

logger: Logger = getLogger(__name__)
router: Router = Router(name=__name__)

@router.message(Command("start"))
async def start_command_handler(message: Message) -> None:
    """Handle the /start command."""
    logger.info("received /start command")
    await message.answer("Привет! Я бот, который будет спрашивать у тебя чем ты занят в течении дня, что бы ты не ленился")

@router.message(Command("help"))
async def help_command_handler(message: Message) -> None:
    """Handle the /help command."""
    logger.info("received /help command")
    await message.answer("Я бот, который будет спрашивать у тебя чем ты занят в течении дня, что бы ты не ленился\n\n"
                         "Вот мой алгоритм работы:\n"
                         "1. Я буду спрашивать у тебя чем ты занят в течении дня\n"
                         "2. Ты будешь отвечать мне да или нет\n"
                         "3. Если ты ответишь да, то я тебе скину фотку кота и в следующий раз спрошу через два часа примерно\n"
                        "4. Если ты ответишь нет, то в следующий раз спрошу через 30 минут примерно\n"
                         )
