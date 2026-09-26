# justluk3s h3re

import asyncio
import html
import os
from dotenv import load_dotenv
import json
import httpx
import questionary

load_dotenv()


def require_env(name: str) -> str:
  value = os.getenv(name)
  if not value:
    raise ValueError(f"Environment variable {name} is required")
  return value

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

if __name__ == "__main__":
  clean_video = []
  choices = []
  
  raw_videos = asyncio.run(search_videos("pizza"))

  for video in raw_videos["items"]:
    clean_video.append(clean_video_item(video))

  for video in clean_video:
    choices.append(
      questionary.Choice(
        title=f"{video['title']} -| {video['channel_title']} -| {video['published_date']}",
        value=video["video_id"]
      )
    )
    
  choice = questionary.select("Choose an option:", choices=choices).ask()
  print(choice)
