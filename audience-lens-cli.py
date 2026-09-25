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

import re
from typing import Optional

load_dotenv()

# Costants
YOUTUBE_REGEX = re.compile(
    r'(?:https?:\/\/)?(?:[a-zA-Z0-9_-]+\.)?youtube\.com\/(?:watch\?(?:[^&\n]*&)*v=|(?:shorts|embed|live)\/)([a-zA-Z0-9_-]{11})|'
    r'(?:https?:\/\/)?youtu\.be\/([a-zA-Z0-9_-]{11})'
)

# Helper Functions

# Helper function to extract video id from raw input text
def extract_video_id(raw_input: str) -> Optional[str]:
    clean_input = raw_input.strip()

    if re.fullmatch(r'[a-zA-Z0-9_-]{11}', clean_input):
        return clean_input

    match = YOUTUBE_REGEX.search(clean_input)
    if match:
        return match.group(1) or match.group(2)
    return None

# Helper function to require environment variables in .env file
def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable {name} is required")
    return value

# Helper function for 
def example_url_video():
    with open("example_url_video.json", "r") as f:
        videos = json.load(f)

    if isinstance(videos, dict):
        videos = list(videos.values())

    max_id = max(video["id"] for video in videos)
    random.seed(time.time_ns())
    selected_id = random.randint(1, max_id)
    return next(video["video_id"] for video in videos if video["id"] == selected_id)

def menu():
    print("audience-lens\n",
        "Discover what your audience is interested about your content!\n")
    while True:
        print("Search for a YouTube video, or paste the URL to get started,",
        f"(e.g. https://youtu.be/czhZ-_QHkjs)")
        raw_input = str(input(" >"))
        video_id = extract_video_id(raw_input)
        if video_id is None:
            print(raw_input)
        else:
            print(video_id)

def main():
    menu()

if __name__ == "__main__":
    main()