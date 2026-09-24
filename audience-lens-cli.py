# justluk3s h3re

# libraries
import os
import json
import random
import time
from dotenv import load_dotenv

import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors

load_dotenv()

# Helper function to require environment variables in .env file
def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable {name} is required")
    return value

def example_url_video():
    with open("example_url_video.json", "r") as f:
        videos = json.load(f)

    if isinstance(videos, dict):
        videos = list(videos.values())

    max_id = max(video["id"] for video in videos)
    random.seed(time.time_ns())
    selected_id = random.randint(1, max_id)
    return next(video["url"] for video in videos if video["id"] == selected_id)

def menu():
    print("audicence-lens")
    print("Discover what your audience is interested about your content!")
    print(f"Search for a YouTube video, or paste the URL to get started (e.g. {example_url_video()})")

def main():
    menu()

if __name__ == "__main__":
    main()