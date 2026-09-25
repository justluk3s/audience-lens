# justluk3s h3re

# libraries
import os
from dotenv import load_dotenv

import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors

import re
from typing import Optional
import html
import asyncio
import httpx

load_dotenv()

# Costants
YOUTUBE_REGEX = re.compile(
    r'(?:https?:\/\/)?(?:[a-zA-Z0-9_-]+\.)?youtube\.com\/(?:watch\?(?:[^&\n]*&)*v=|(?:shorts|embed|live)\/)([a-zA-Z0-9_-]{11})|'
    r'(?:https?:\/\/)?youtu\.be\/([a-zA-Z0-9_-]{11})')

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

async def search_videos(query: str, max_results: int = 10):
  url = "https://www.googleapis.com/youtube/v3/search"
  params = {
      "part": "snippet",
      "q": query,
      "type": "video",
      "maxResults": max_results,
      "key": require_env("YOUTUBE_API_KEY"),
  }

  async with httpx.AsyncClient() as client:
    response = await client.get(url, params=params)
    response.raise_for_status()
    return response.json()

def clean_video_item(item: dict) -> dict:
  snippet = item.get("snippet", {})

  # 1. "2025-10-10T12:00:20Z" -> split by "T" -> "2025-10-10"
  published_raw = snippet.get("publishedAt", "")
  published_date = published_raw.split("T")[0] if "T" in published_raw else ""

  # 2. Get thumbnail URL (prefer medium, fallback to default)
  thumbnails = snippet.get("thumbnails", {})
  thumbnail_url = (
      thumbnails.get("medium", {}).get("url")
      or thumbnails.get("default", {}).get("url")
      or ""
  )

  return {
    "title": html.unescape(snippet.get("title", "")),
    "channel_title": html.unescape(snippet.get("channelTitle", "")),
    "published_date": published_date,
    "video_id": item.get("id", {}).get("videoId"),
    "thumbnail_url": thumbnail_url,
  }
  
def video_string_print(item: dict) -> str:
    return(f"{item["title"]} -| {item["channel_title"]} -| {item["published_date"]}")


# Helper function to require environment variables in .env file
def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable {name} is required")
    return value

def menu():
    print("audience-lens\n",
        "Discover what your audience is interested about your content!\n")
    while True:
        print("Search for a YouTube video, or paste the URL to get started (e.g. https://youtu.be/czhZ-_QHkjs)")
        raw_input = str(input(" >"))
        video_id = extract_video_id(raw_input)
        if video_id is None:
            data = asyncio.run(search_videos(raw_input))
            for video in data["items"]:
                cleaned_item = clean_video_item(video)
                print(video_string_print(cleaned_item))
        else:
            print(video_id)

def main():
    menu()

if __name__ == "__main__":
    main()