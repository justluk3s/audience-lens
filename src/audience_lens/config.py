# justluk3s h3re

# libraries
import os
from dotenv import load_dotenv

# functions
load_dotenv()

# Helper function to require environment variables from .env file
def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable {name} is required")
    return value

# Define settings here
YOUTUBE_API_KEY: str = require_env("YOUTUBE_API_KEY")