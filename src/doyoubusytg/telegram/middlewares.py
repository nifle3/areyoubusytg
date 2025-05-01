from typing import Callable, Dict, Any, Awaitable, Protocol
from logging import getLogger, Logger

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


logger: Logger = getLogger(__name__)


class ChatIdRepo(Protocol):
    async def add_chat_id(self, chat_id: int) -> None:
        """Add a chat ID to the database."""

    async def check_chat_id(self, chat_id: int) -> bool:
        """Check if a chat ID exists in the database."""


class CheckSaveUserMiddleware(BaseMiddleware):
    def __init__(self, chat_id_repo: ChatIdRepo) -> None:
        super().__init__()
        self.chat_id_repo = chat_id_repo

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: Dict[str, Any]) -> Any:
        """Middleware to check if the user is saved in the database."""
        if hasattr(event, 'chat') and event.chat is not None:
            chat_id = event.chat.id
            is_chat_exists = await self.chat_id_repo.check_chat_id(chat_id)

            if not is_chat_exists:
                await self.chat_id_repo.add_chat_id(chat_id)
                logger.info(f"Chat ID {chat_id} added to the database.")
    
        return await handler(event, data)
