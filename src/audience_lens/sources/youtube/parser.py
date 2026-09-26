# justluk3s h3re

# libraries
import re

YOUTUBE_REGEX = re.compile(
    r'(?:https?:\/\/)?(?:[a-zA-Z0-9_-]+\.)?youtube\.com\/(?:watch\?(?:[^&\n]*&)*v=|(?:shorts|embed|live)\/)([a-zA-Z0-9_-]{11})|'
    r'(?:https?:\/\/)?youtu\.be\/([a-zA-Z0-9_-]{11})')

def extract_video_id(raw_input: str) -> str | None:
    clean_input = raw_input.strip()

    # Direct 11-character YouTube video ID
    if re.fullmatch(r'[a-zA-Z0-9_-]{11}', clean_input):
        return clean_input

    match = YOUTUBE_REGEX.search(clean_input)
    if match:
        return match.group(1) or match.group(2)
    return None