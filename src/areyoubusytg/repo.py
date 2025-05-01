from logging import getLogger, Logger
from asyncio import Lock
from datetime import datetime, timedelta

from tinydb import TinyDB, Query
from tinydb.table import Document
import json

from user import User

logger: Logger = getLogger(__name__)

class TinyDbRepo:
    def __init__(self, db_name: str):
        self._db = TinyDB(db_name)
        self._lock = Lock()

    async def add_chat_id(self, chat_id: int) -> None:
        """Add a chat ID to the database."""
        async with self._lock:
            query = Query()
            user = User(chat_id=chat_id, is_busy=False, last_message=datetime.now())
            self._db.insert(Document(user.to_document(), doc_id=chat_id))
            logger.debug("Chat ID %d added to the database", chat_id)

    async def check_chat_id(self, chat_id: int) -> bool:
        """Check if a chat ID exists in the database."""
        async with self._lock:
            query = Query()

            exists = self._db.contains(query.chat_id == chat_id)
            logger.debug("Chat ID %d exists: %s", chat_id, exists)

            return exists

    async def get_users(self, current: datetime, is_busy_delta: timedelta, is_not_busy_delta: timedelta) -> list[User]:
        async with self._lock:
            query_busy = Query()
            query_not_busy = Query()

            busy_users = self._db.search(
                (query_busy.is_busy == True) &
                (query_busy.last_message.map(lambda x: datetime.fromisoformat(x)) < current - is_busy_delta)
            )

            not_busy_users = self._db.search(
                (query_not_busy.is_busy == False) &
                (query_not_busy.last_message.map(lambda x: datetime.fromisoformat(x)) < current - is_not_busy_delta)
            )

            users = busy_users + not_busy_users
            logger.debug("Found %d users", len(users))

            return [User.from_document(user) for user in users]

    async def update_user(self, user: User) -> None:
        async with self._lock:
            self._db.upsert(user.to_dict(), doc_id=user.chat_id)
            logger.debug("User %s updated", user.chat_id)
