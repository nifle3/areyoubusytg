from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    """A class to represent a user."""

    chat_id: int
    last_message: datetime
    is_busy: bool = False
