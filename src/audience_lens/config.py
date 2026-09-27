
import os
from dotenv import load_dotenv

load_dotenv()


def require_env(name: str) -> str:
    """Retrieve an environment variable or raise an informative error."""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable '{name}' is required")
    return value


YOUTUBE_API_KEY: str = require_env("YOUTUBE_API_KEY")