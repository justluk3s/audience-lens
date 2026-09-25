import os
import json
from dotenv import load_dotenv

import googleapiclient.discovery

load_dotenv()

def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable {name} is required")
    return value

def main():
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=require_env("YOUTUBE_API_KEY"))

    print("audience-lens")
    print("Discover what your audience is interested about your content!")
    video_id = input("Enter the ID of a YouTube video (e.g. TIZRskDMyA4):\n> ")

    items = []
    page_token = None

    # Fetch every page of top-level comment threads.
    while True:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=page_token,
        ).execute()

        for thread in response.get("items", []):
            top_level_comment = thread["snippet"]["topLevelComment"]
            items.append(top_level_comment)

            # Replies require a separate paginated request to guarantee that
            # all replies are returned, rather than only the embedded subset.
            reply_token = None
            while True:
                replies = youtube.comments().list(
                    part="snippet",
                    parentId=top_level_comment["id"],
                    maxResults=100,
                    pageToken=reply_token,
                ).execute()
                items.extend(replies.get("items", []))
                reply_token = replies.get("nextPageToken")
                if not reply_token:
                    break

        page_token = response.get("nextPageToken")
        if not page_token:
            break

    print(len(items), "comments found")
    print(json.dumps(items, indent=2))

if __name__ == "__main__":
    main()