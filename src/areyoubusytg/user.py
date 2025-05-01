from dataclasses import dataclass
from datetime import datetime

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
    def from_document(self, document: dict) -> None:
        """Load the User object from a dictionary."""
        self.chat_id = document["chat_id"]
        self.last_message = datetime.fromisoformat(document["last_message"])
        self.is_busy = document["is_busy"]
