import os
from errors import ConfigError

def get_env(key: str, default: str = None) -> str:
    """Get the environment variable or return a default value."""
    env = os.getenv(key, default)
    if env is None:
        raise ConfigError(key)
    
    return env
