
import asyncio

import questionary

from audience_lens.sources import youtube
from audience_lens.cli.ui import (
    display_transcript,
    prompt_search_input,
    prompt_video_selection,
)

# Registered video source providers
ACTIVE_SOURCES = {
    "YouTube": youtube,
}




# =====================================================
# UI / Questionary Helpers
# =====================================================
def format_choice_label(video: dict) -> str:
    """Format a clean, readable label with provider for terminal selection."""
    provider = video.get("provider", "UNKNOWN").upper()
    title = video.get("title", "Untitled")
    channel = video.get("channel_title", "Unknown Channel")
    published_at = video.get("published_at", "")
    date = published_at.split("T")[0] if "T" in published_at else published_at
    return f"[{provider}] {title} | {channel} ({date})"

async def prompt_search_input() -> str | None:
    """Prompt the user for a search term, direct URL, or video ID."""
    answer = await questionary.text("Search video or paste URL / ID:").ask_async()
    if not answer or not answer.strip():
        return None
    return answer.strip()

async def prompt_video_selection(videos: list[dict]) -> tuple[str, str] | None:
    """Present a list of parsed video dictionaries for interactive selection."""
    choices = [
        questionary.Choice(
            title=format_choice_label(v),
            value=(v["provider"], v["video_id"]),
        )
        for v in videos
        if v.get("video_id")
    ]

    if not choices:
        return None

    return await questionary.select(
        "Select a video to analyze:",
        choices=choices,
    ).ask_async()

def display_transcript(
    formatted_text: str,
    max_lines: int | None = 25,
) -> None:
    """Print formatted transcript lines clearly in the terminal."""
    print("\n VIDEO TRANSCRIPT",
          "=" * 60,"\n")

    lines = formatted_text.splitlines()
    if max_lines and len(lines) > max_lines:
        for line in lines[:max_lines]:
            print(f"  {line}")
        print(f"\n  ... and {len(lines) - max_lines} more lines.")
    else:
        for line in lines:
            print(f"  {line}")

    print("=" * 60 + "\n")



# =====================================================
# Provider & Search Logic
# =====================================================

def resolve_direct_input(
    raw_input: str,
) -> tuple[str, str] | tuple[None, None]:
    """
    Check sources to see if raw_input is a valid direct URL for a video.

    Returns (provider_name, item_id) or (None, None).
    """
    for source in ACTIVE_SOURCES.values():
        item_id = source.extract_video_id(raw_input)
        if item_id:
            return source.PROVIDER_NAME, item_id
    return None, None

async def search_all_sources(query: str, max_results: int = 10) -> list[dict]:
    """Query active sources and return normalized video items."""
    tasks = [
        source.search_videos(query, max_results=max_results)
        for source in ACTIVE_SOURCES.values()
    ]
    # Fetch all platforms at the same time
    source_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    results = []
    for items in source_results:
        if isinstance(items, list):
            results.extend(items)
    return results

async def find_video() -> tuple[str, str] | tuple[None, None]:
    """
    Orchestrate video discovery: prompt, verify direct IDs/URLs, or search.
    """
    clean_input = await prompt_search_input()
    if not clean_input:
        print("No input provided. Exiting.")
        return None, None

    # 1. Direct URL check
    provider, direct_id = resolve_direct_input(clean_input)
    if provider and direct_id:
        return provider, direct_id

    # 2. Search query across providers
    print(f"\n Searching on multiple platforms for: '{clean_input}'...")
    videos = await search_all_sources(clean_input, max_results=10)
    if not videos:
        print("No videos found matching your query.")
        return None, None
    selected = await prompt_video_selection(videos)
    if not selected:
        print("Selection cancelled.")
        return None, None

    return selected

async def run_cli() -> None:
    """Run the main interactive CLI session."""
    print(" 🔍 Audience Lens",
          " Discover what your audience is saying about your content!")

    provider, video_id = await find_video()
    if not video_id:
        return

    print(f"\n Video found from: {provider} with ID: {video_id}")
    source = ACTIVE_SOURCES[provider]
    
    print("\n Fetching transcript...")
    raw_transcript = await source.get_video_transcript(video_id)
    if raw_transcript:
        formatted = source.format_transcript_lines(
            raw_transcript,
            with_timestamps=True,
        )
        display_transcript(formatted, max_lines=25)

def main() -> None:
    """Entry point for audience-lens CLI command."""
    try:
        asyncio.run(run_cli())
    except KeyboardInterrupt:
        print("\nAborted by user.")


if __name__ == "__main__":
    main()
