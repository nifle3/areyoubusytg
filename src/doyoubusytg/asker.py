from typing import Protocol
from datetime import datetime, timedelta

from user import User


class BotSender(Protocol):
    """A protocol for a bot sender."""

    async def send_message(self, chat_id: int, message: str) -> None:
        """Send a message to a user."""
        pass


class UserRepo(Protocol):
    """A protocol for a user repository."""

    async def get_users(self, current: datetime, is_busy_delta: timedelta, is_not_busy_delta: timedelta) -> list[User]:
        """Get a list of users with last message timestamp."""
    
    async def update_user(self, user: User) -> None:
        """Update a user."""


class Asker:
    """A class to manage the scheduling of sending message to user."""

    def __init__(self, bot_sender: BotSender, user_repo: UserRepo) -> None:
        self._bot_sender = bot_sender
        self._user_repo = user_repo
        self._is_busy_delta = timedelta(minutes=90)
        self._is_not_busy_delta = timedelta(minutes=30)
        self._sended_message = "Привет ты занят?"

    async def __call__(self):
        """Ask the user if they are busy."""
        now = datetime.now()
        users = await self._user_repo.get_users(now, self._is_busy_delta, self._is_not_busy_delta)
        for user in users:
            await self._bot_sender.send_message(user.chat_id, self._sended_message)
            user.last_message = now
            await self._user_repo.update_user(user)
