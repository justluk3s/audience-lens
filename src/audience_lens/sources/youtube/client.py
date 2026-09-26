# justluk3s h3re

# libraries
import html
import httpx
from audience_lens.config import YOUTUBE_API_KEY

# Function to query videos from a string
async def search_videos(query: str, max_results: int = 10):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
        # Selecting only useful fields:
        "fields": "items(id/videoId,snippet(title,publishedAt,channelTitle,thumbnails))",
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

def extract_video_data(item: dict) -> dict:
    snippet = item.get("snippet", {})
    # Extract thumbnails mapping each size to its URL and dimensions
    thumbnails_raw = snippet.get("thumbnails", {})
    thumbnails = {
        name: {
            "url": thumb["url"],
            "width": thumb["width"],
            "height": thumb["height"],
        }
        for name, thumb in thumbnails_raw.items()
        if "url" in thumb
    }
    return {
        "video_id": item.get("id", {}).get("videoId"),
        "title": html.unescape(snippet.get("title", "")),  # unescapes &#39;, &amp;, etc.
        "channel_title": html.unescape(snippet.get("channelTitle", "")),
        "published_at": snippet.get("publishedAt", ""),
        "thumbnails": thumbnails,
    }