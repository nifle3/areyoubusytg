class ConfigError(Exception):
    """Base class for configuration-related errors."""

    def __init__(self, key: str):
        self._key = key

    def __str__(self):
        return f"Env variable not set: {self._key}"


class UserBlockedBot(Exception):
    """Exception that raised then user blocked bot"""

class CatServiceUnavailable(Exception):
    pass
