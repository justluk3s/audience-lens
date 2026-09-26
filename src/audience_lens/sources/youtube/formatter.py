# justluk3s h3re

import html
import re

YOUTUBE_REGEX = re.compile(
    r"(?:https?:\/\/)?(?:[a-zA-Z0-9_-]+\.)?youtube\.com\/"
    r"(?:watch\?(?:[^&\n]*&)*v=|(?:shorts|embed|live)\/)([a-zA-Z0-9_-]{11})|"
    r"(?:https?:\/\/)?youtu\.be\/([a-zA-Z0-9_-]{11})"
)


def extract_video_id(raw_input: str) -> str | None:
    """Extract an 11-character YouTube video ID from a URL or raw ID string."""
    clean_input = raw_input.strip()

    if re.fullmatch(r"[a-zA-Z0-9_-]{11}", clean_input):
        return clean_input

    match = YOUTUBE_REGEX.search(clean_input)
    if match:
        return match.group(1) or match.group(2)
    return None


def extract_video_data(item: dict) -> dict:
    """Format and clean a raw video search snippet from YouTube API."""
    snippet = item.get("snippet", {})
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
        "title": html.unescape(snippet.get("title", "")),
        "channel_title": html.unescape(snippet.get("channelTitle", "")),
        "published_at": snippet.get("publishedAt", ""),
        "thumbnails": thumbnails,
    }


def format_seconds(seconds: float) -> str:
    """Convert seconds to MM:SS or HH:MM:SS format."""
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_transcript_lines(
    snippets: list[dict],
    with_timestamps: bool = True,
) -> str:
    """Format raw snippet dicts from youtube-transcript-api into readable text lines."""
    if not snippets:
        return "No transcript content available."

    lines = []
    for s in snippets:
        text = s.get("text", "").replace("\n", " ").strip()
        if with_timestamps:
            timestamp = format_seconds(s.get("start", 0.0))
            lines.append(f"[{timestamp}] {text}")
        else:
            lines.append(text)

    return "\n".join(lines)