from logging import Filter
import contextvars
import uuid

class IdContextFilter(Filter):
    """Filter to add a context id variable to log records."""

    def __init__(self, name: str):
        super().__init__(name)
        self.var = contextvars.ContextVar(name)

    def filter(self, record) -> bool:
        record.id = self.var.get()
        return True

    def set_id(self, id: uuid.UUID) -> None:
        """Set the context id."""
        self.var.set(id)
