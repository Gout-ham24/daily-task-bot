"""
SILVER Task — News Headline Fetcher
Scrapes 3 news websites using FREE RSS feeds.
No API key needed — works perfectly on GitHub Actions.
Sources: Google News India, NDTV, Times of India
Includes: source links + publication times
"""

import datetime
import re
from collections import Counter
import feedparser

STOP_WORDS = {
    "the", "a", "an", "in", "on", "at", "to", "of", "and", "or", "is",
    "are", "was", "were", "for", "with", "by", "from", "that", "this",
    "it", "its", "as", "be", "has", "have", "had", "but", "not", "no",
    "he", "she", "they", "we", "you", "i", "my", "his", "her", "their",
    "will", "can", "do", "did", "into", "over", "after", "says", "said",
    "new", "up", "out", "india", "indian", "news", "amid", "after",
}

RSS_FEEDS = [
    {
        "name": "Google News India",
        "url": "https://news.google.com/rss/headlines/section/geo/IN?hl=en-IN&gl=IN&ceid=IN:en",
    },
    {
        "name": "NDTV",
        "url": "https://feeds.feedburner.com/ndtvnews-india-news",
    },
    {
        "name": "Times of India",
        "url": "https://timesofindia.indiatimes.com/rss/4719148.cms",
    },
]

MAX_PER_FEED = 5


def parse_pub_date(entry) -> str:
    """Extract and format the publication time from a feed entry."""
    try:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            dt = datetime.datetime(*entry.published_parsed[:6])
            return dt.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        pass
    return ""


def extract_trends(headlines: list, top_n: int = 5) -> list:
    words = []
    for h in headlines:
        tokens = re.findall(r"\b[a-zA-Z]{4,}\b", h.lower())
        words.extend(t for t in tokens if t not in STOP_WORDS)
    counter = Counter(words)
    return [word.title() for word, _ in counter.most_common(top_n)]


def get_news_data() -> dict:
    all_headlines = []

    for feed_info in RSS_FEEDS:
        source = feed_info["name"]
        try:
            feed = feedparser.parse(feed_info["url"])
            entries = feed.entries[:MAX_PER_FEED]

            for entry in entries:
                title = entry.get("title", "").strip()
                link  = entry.get("link", "").strip()

                # Clean "Headline - Source Name" format (Google News style)
                if " - " in title:
                    title = title.rsplit(" - ", 1)[0].strip()

                pub_time = parse_pub_date(entry)

                if title:
                    all_headlines.append({
                        "title":      title,
                        "source":     source,
                        "url":        link,
                        "published":  pub_time,
                    })

            print(f"      ✅ {source}: {len(entries)} headlines fetched")

        except Exception as e:
            print(f"      ⚠  {source} failed: {e}")

    trends = extract_trends([h["title"] for h in all_headlines])

    return {
        "headlines":  all_headlines,
        "trends":     trends,
        "total":      len(all_headlines),
        "fetched_at": datetime.datetime.now().strftime("%d %b %Y, %I:%M %p IST"),
    }
