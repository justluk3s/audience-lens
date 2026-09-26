# 🔍 Audience Lens

> A tool to discover, ingest, and analyze audience discussions and sentiment from video platforms.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://peps.python.org/pep-0008/)

> [!NOTE]
> **Active Development Status**: Audience Lens is in early active development. Currently, the project provides an interactive CLI for **video discovery, URL/ID parsing, and multi-source video resolution**. The comment ingestion pipeline, local caching, and sentiment/topic analysis are currently in progress.

---

## 🎯 Current Status vs. Future Vision

To make expectations crystal clear, here is what is working right now versus what is on the roadmap:

### ✅ Available Today
- **Interactive CLI Video Finder**: Run `audience-lens` to interactively search videos or paste URLs.
- **Smart URL & Video ID Parsing**: Extracts 11-char video IDs instantly from YouTube watch URLs, Shorts, embed links, and `youtu.be` shortcuts without wasting API quota.
- **Quota-Optimized Search Client**: Async HTTP client using `httpx` with strict Google API `fields` filtering to keep network payloads lightweight.
- **Modular Multi-Provider Design**: The architecture is decoupled so new sources (e.g., TikTok) can plug in with standard `extract_video_id` and `search_videos` interfaces.

### ⏳ In Active Development (Next Steps)
- **High-Throughput Comment Ingestion**: Downloading full top-level comment threads and nested reply chains concurrently.
- **Local Caching & Storage**: Saving video comments into SQLite / JSON snapshots so you never burn quota re-analyzing the same video.
- **Analysis Engine**: NLP-driven sentiment analysis, theme/keyword extraction, and audience question identification.

### 🌐 Product Vision (Future Interfaces)
- **Public Demo Website**: A hosted showcase site featuring pre-analyzed benchmark videos where anyone can browse the analytics without needing an API key.
- **Recruiter & Evaluator Access**: A token-authenticated section on the hosted site allowing hiring managers and evaluators to run live queries on arbitrary videos using a private evaluation quota.
- **Local Web Server (Self-Hosted)**: Anyone cloning this repo will be able to launch the web dashboard locally using their own YouTube API key to experience the full GUI.

---

## 📁 Repository Structure

```text
audience-lens/
├── src/
│   └── audience_lens/
│       ├── cli/               # Terminal interface & interactive prompts
│       ├── models/            # Data schemas (in progress)
│       ├── sources/           # Video platform connectors
│       │   └── youtube/       # YouTube async client & regex URL parser
│       ├── config.py          # Environment & API key validation
│       └── __init__.py
├── docs/                      # Architectural decisions & design notes
│   └── architecture_decisions.md
├── pyproject.toml             # Package metadata, dependencies, & entry points
├── .env.example               # Environment variables template
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10 or higher
- A [YouTube Data API v3 key](https://developers.google.com/youtube/v3/getting-started)

### 2. Installation

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/justluk3s/audience-lens.git
cd audience-lens

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e .
```

### 3. Configuration

Copy the example environment file and add your YouTube Data API key:

```bash
cp .env.example .env
```

In `.env`:
```ini
YOUTUBE_API_KEY="your_actual_youtube_api_key"
```

---

## 💻 What You Can Do Right Now

### 1. Run the Interactive CLI

Launch the interactive prompt to search for videos or paste a URL/ID:

```bash
audience-lens
```

*(Alternatively: `python -m audience_lens.cli.app`)*

The CLI will:
1. Ask you for a search term, YouTube URL, or video ID.
2. If you paste a URL or video ID, it resolves it immediately.
3. If you type a search term, it queries the API and lets you select a video using your arrow keys.

### 2. Use as a Python Library

You can import and use the modular providers in your own scripts:

```python
import asyncio
from audience_lens.sources import youtube

async def main():
    # 1. Parse any YouTube URL format (watch, shorts, youtu.be, embed)
    video_id = youtube.extract_video_id("https://youtu.be/kCoHipbcXFo")
    print("Resolved ID:", video_id)

    # 2. Search videos asynchronously
    results = await youtube.search_videos("machine learning", max_results=3)
    for item in results.get("items", []):
        video = youtube.extract_video_data(item)
        print(f"[{video['video_id']}] {video['title']} by {video['channel_title']}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🛠️ Architecture & Decisions

For detailed design notes regarding quota economics, why `httpx` was chosen over Google SDK, and the multi-interface roadmap, see:

👉 **[Architecture & Design Decisions](docs/architecture_decisions.md)**

---

## 🗺️ Roadmap

- [x] YouTube search and video metadata extraction
- [x] URL and video ID parsing (standard, shorts, embed, youtu.be)
- [x] Async HTTP client with API field filtering
- [x] Interactive terminal selector (`audience-lens` command)
- [ ] Paginated comment and reply ingestion pipeline
- [ ] Local caching & storage (SQLite / JSON) to prevent duplicate API calls
- [ ] Sentiment, topic, and question analysis engine
- [ ] Local web server with graphical UI
- [ ] Hosted demo site with token-gated recruiter access

---

## 🤝 Contributing

Contributions and feedback are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.