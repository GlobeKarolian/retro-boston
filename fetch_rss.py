import os
import json
import time
from datetime import datetime, timezone
import feedparser
import html
import re
import sys

RSS_URL = os.getenv("RSS_URL", "https://boston.com/bdc-msn-rss")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "articles.json")
MAX_ITEMS = int(os.getenv("MAX_ITEMS", "40"))

def strip_tags(text: str) -> str:
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def normalize_entry(entry):
    title = entry.get("title", "").strip()
    link = entry.get("link", "").strip()
    description = entry.get("summary", entry.get("description", "")) or ""
    pub = entry.get("published", entry.get("updated", "")) or ""
    if not pub and entry.get("published_parsed"):
        pub = time.strftime("%a, %d %b %Y %H:%M:%S %z", entry["published_parsed"])
    elif not pub and entry.get("updated_parsed"):
        pub = time.strftime("%a, %d %b %Y %H:%M:%S %z", entry["updated_parsed"])
    return { "title": title, "link": link, "description": description, "pubDate": pub }

def main():
    print(f"Fetching RSS from: {RSS_URL}")
    feed = feedparser.parse(RSS_URL)
    if feed.bozo:
        print(f"Warning: feed parsing raised an error: {feed.bozo_exception}", file=sys.stderr)
    entries = feed.get("entries", [])[:MAX_ITEMS]
    articles = [normalize_entry(e) for e in entries if e.get("link")]
    payload = { "lastUpdated": datetime.now(timezone.utc).isoformat(), "articles": articles }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(articles)} articles to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
