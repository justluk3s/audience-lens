import asyncio

import httpx
from requests import Session
from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    YouTubeTranscriptApi,
)

from audience_lens.config import YOUTUBE_API_KEY
from audience_lens.sources.youtube.formatter import extract_video_data


async def search_videos(query: str, max_results: int = 10) -> list[dict]:
    """Query YouTube search endpoint for video metadata."""
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
        "fields": "items(id/videoId,snippet(title,publishedAt,channelTitle,thumbnails))",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("items", []):
            parsed = extract_video_data(item)
            parsed["provider"] = "YouTube"
            results.append(parsed)
        return results


def get_transcript_session() -> Session:
    """Create a requests session mimicking a desktop browser."""
    session = Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9,it;q=0.8",
        "Sec-Fetch-Mode": "navigate",
    })
    return session


async def get_video_transcript(
    video_id: str,
    target_language: str = "en",
) -> list[dict] | None:
    """
    Fetch the transcript for a YouTube video.

    1. Checks for direct target language or common variants.
    2. Falls back to translating any available transcript.
    3. Falls back to the last available raw transcript if translation fails.
    """
    def _fetch():
        session = get_transcript_session()
        ytt_api = YouTubeTranscriptApi(http_client=session)

        try:
            transcript_list = ytt_api.list(video_id)

            try:
                transcript = transcript_list.find_transcript(
                    [target_language, "en-US", "en-GB"]
                )
            except NoTranscriptFound:
                available_transcripts = list(transcript_list)
                if not available_transcripts:
                    print(f"⚠️ No transcripts available for video '{video_id}'.")
                    return None

                transcript = None
                for t in available_transcripts:
                    if t.is_translatable:
                        transcript = t.translate(target_language)
                        break

                if transcript is None:
                    transcript = available_transcripts[-1]

            return transcript.fetch().to_raw_data()

        except TranscriptsDisabled:
            print(f"⚠️ Transcripts are disabled for video '{video_id}'.")
            return None
        except VideoUnavailable:
            print(f"⚠️ Video '{video_id}' is unavailable (private or deleted).")
            return None
        except Exception as e:
            print(f"⚠️ Could not retrieve transcript for video '{video_id}': {e}")
            return None

    return await asyncio.to_thread(_fetch)
