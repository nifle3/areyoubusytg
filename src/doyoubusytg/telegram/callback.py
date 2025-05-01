from typing import Protocol
from logging import getLogger

from aiogram import Router, F
from aiogram.types import CallbackQuery

class Repo(Protocol):
    async def set_user_state(self, user_id: int, is_bust: bool) -> None:
        """Set the user state in the database."""


logger = getLogger(__name__)
router = Router(name=__name__)


@router.callback_query(F.data == "yes")
async def yes_callback_handler(callback: CallbackQuery, repo: Repo) -> None:
    """Handle the 'yes' callback."""
    user_id = callback.from_user.id
    await repo.set_user_state(user_id, True)
    await callback.answer("Отлично! Вот тебе фотка кота!")

@router.callback_query(F.data == "no")
async def no_callback_handler(callback: CallbackQuery, repo: Repo) -> None:
    """Handle the 'no' callback."""
    user_id = callback.from_user.id
    await repo.set_user_state(user_id, False)
    await callback.answer("За работу!")