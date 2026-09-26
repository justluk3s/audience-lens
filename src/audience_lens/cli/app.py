# justluk3s h3re

import asyncio

import questionary

from audience_lens.sources import youtube

# Registered video source providers
ACTIVE_SOURCES = [youtube]


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


# =====================================================
# Provider & Search Logic
# =====================================================

def resolve_direct_input(
    raw_input: str,
) -> tuple[str, str] | tuple[None, None]:
    """
    Check registered sources to see if raw_input is a valid direct URL or ID.

    Returns (provider_name, item_id) or (None, None).
    """
    for source in ACTIVE_SOURCES:
        item_id = source.extract_video_id(raw_input)
        if item_id:
            return source.PROVIDER_NAME, item_id
    return None, None


async def search_all_sources(query: str, max_results: int = 10) -> list[dict]:
    """Query active sources and return normalized video items."""
    results = []

    try:
        yt_data = await youtube.search_videos(query, max_results=max_results)
        for item in yt_data.get("items", []):
            parsed = youtube.extract_video_data(item)
            parsed["provider"] = youtube.PROVIDER_NAME
            results.append(parsed)
    except Exception as e:
        print(f"Error fetching YouTube search results: {e}")

    return results


# =====================================================
# Main Orchestration & Display
# =====================================================

async def select_or_find_video() -> tuple[str, str] | tuple[None, None]:
    """
    Orchestrate video discovery: prompt, verify direct IDs/URLs, or search.
    """
    clean_input = await prompt_search_input()
    if not clean_input:
        print("No input provided. Exiting.")
        return None, None

    # 1. Direct URL or ID check
    provider, direct_id = resolve_direct_input(clean_input)
    if provider and direct_id:
        return provider, direct_id

    # 2. Search query across providers
    print(f"\n🔍 Searching for: '{clean_input}'...")
    videos = await search_all_sources(clean_input, max_results=10)
    if not videos:
        print("No videos found matching your query.")
        return None, None

    # 3. Interactive prompt to pick from results
    selected = await prompt_video_selection(videos)
    if not selected:
        print("Selection cancelled.")
        return None, None

    return selected


def display_transcript(
    formatted_text: str,
    max_lines: int | None = 25,
) -> None:
    """Print formatted transcript lines clearly in the terminal."""
    print("\n" + "=" * 60)
    print(" 📜 VIDEO TRANSCRIPT")
    print("=" * 60)

    lines = formatted_text.splitlines()
    if max_lines and len(lines) > max_lines:
        for line in lines[:max_lines]:
            print(f"  {line}")
        print(f"\n  ... and {len(lines) - max_lines} more lines.")
    else:
        for line in lines:
            print(f"  {line}")

    print("=" * 60 + "\n")


async def run_cli() -> None:
    """Run the main interactive CLI session."""
    print("=" * 60)
    print(" 🔍 Audience Lens")
    print(" Discover what your audience is saying about your content!")
    print("=" * 60 + "\n")

    provider, video_id = await select_or_find_video()
    if not video_id:
        return

    print(f"\n✅ Provider: {provider}")
    print(f"✅ Video ID: {video_id}")

    # Fetch and display transcript
    print("\n⏳ Fetching transcript...")
    raw_transcript = youtube.get_video_transcript(video_id)
    if raw_transcript:
        formatted = youtube.format_transcript_lines(
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
