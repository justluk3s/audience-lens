import questionary


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
          "=" * 60, "\n")

    lines = formatted_text.splitlines()
    if max_lines and len(lines) > max_lines:
        for line in lines[:max_lines]:
            print(f"  {line}")
        print(f"\n  ... and {len(lines) - max_lines} more lines.")
    else:
        for line in lines:
            print(f"  {line}")
    print("=" * 60 + "\n")
