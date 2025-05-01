from typing import Protocol
from logging import getLogger

from aiogram import Router, F
from aiogram.types import CallbackQuery

from areyoubusytg.cat_image_service import CatImageAPI

class Repo(Protocol):
    async def set_user_state(self, user_id: int, is_bust: bool) -> None:
        """Set the user state in the database."""


logger = getLogger(__name__)
router = Router(name=__name__)


@router.callback_query(F.data == "yes")
async def yes_callback_handler(callback: CallbackQuery, repo: Repo, cat_image: CatImageAPI) -> None:
    """Handle the 'yes' callback."""
    logger.info("received 'yes' callback")
    user_id = callback.from_user.id
    await repo.set_user_state(user_id, True)
    await callback.answer("Отлично! Вот тебе фотка кота!")
    await callback.message.delete()
    cat_image_url = await cat_image.get_cat_image()
    await callback.message.answer_photo(
        cat_image_url,
        caption="Вот тебе котик!",
    )


@router.callback_query(F.data == "no")
async def no_callback_handler(callback: CallbackQuery, repo: Repo) -> None:
    """Handle the 'no' callback."""
    logger.info("received 'no' callback")
    user_id = callback.from_user.id
    await repo.set_user_state(user_id, False)
    await callback.answer("За работу!")
    await callback.message.delete_reply_markup()
    await callback.message.delete()
