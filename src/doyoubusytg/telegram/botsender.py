from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class TelegramBotSender:
    """A class to send messages to a user."""

    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self._profile_kb = InlineKeyboardMarkup([[
            InlineKeyboardButton(text=answer, callback_data=answer) for answer in ["Yes", "No"]
        ]], row_width=1)

    async def send_message(self, chat_id: int, message: str, answers: list[str]) -> None:
        """Send a message to a user."""
        await self._bot.send_message(chat_id, message, reply_markup=self._profile_kb)