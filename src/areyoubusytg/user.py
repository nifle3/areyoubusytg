from dataclasses import dataclass
from datetime import datetime
from typing import Self


@dataclass
class User:
    """A class to represent a user."""

    chat_id: int
    last_message: datetime
    is_busy: bool = False

    def to_document(self) -> dict:
        """Convert the User object to a dictionary."""
        return {
            "chat_id": self.chat_id,
            "last_message": self.last_message.isoformat(),
            "is_busy": self.is_busy,
        }

    @classmethod
    def from_document(cls, document: dict) -> Self:
        """Load the User object from a dictionary."""
        return cls(
            chat_id=document["chat_id"],
            last_message=datetime.fromisoformat(document["last_message"]),
            is_busy=document.get("is_busy", False)
        )
