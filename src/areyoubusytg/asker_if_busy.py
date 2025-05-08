from typing import Protocol
from datetime import datetime, timedelta
from logging import getLogger, Logger
import uuid

from user import User

logger: Logger = getLogger(__name__)

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


class ContextVarSetter(Protocol):
    def set_id(self, value: uuid.UUID) -> None:
        """Set the context variable."""

class Asker:
    """A class to manage the scheduling of sending message to user."""

    def __init__(self, bot_sender: BotSender, user_repo: UserRepo) -> None:
        self._bot_sender = bot_sender
        self._user_repo = user_repo
        self._is_busy_delta = timedelta(minutes=60)
        self._is_not_busy_delta = timedelta(minutes=30)
        self._sended_message = "Привет ты занят?"

    async def ask(self):
        """Ask the user if they are busy."""
        logger.debug("Asking start")

        now = datetime.now()
        users = await self._user_repo.get_users(now, self._is_busy_delta, self._is_not_busy_delta)
        logger.info("Users to ask: %d", len(users))
        for user in users:
            logger.debug("Asking user %d", user.chat_id)
            try:
                await self._bot_sender.send_message(user.chat_id, self._sended_message)
            except Exception as e:
                logger.exception("Error sending message to user")
                continue

            user.last_message = now
            await self._user_repo.update_user(user)

        logger.debug("Asking end")


class AskerDecorator:
    """A decorator to set the context variable for the Asker class."""

    def __init__(self, context_var_setter: ContextVarSetter, asker: Asker) -> None:
        self._context_var_setter = context_var_setter
        self._asker = asker

    def ask(self) -> None:
        id = uuid.uuid5()
        self._context_var_setter.set_id(id)
        logger.debug(f"Setting context ID: {id}")
        self._asker.ask()
