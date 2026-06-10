"""
SILVER Task — News Headline Fetcher
Fetches top India headlines using NewsAPI and extracts keyword trends.
"""

import os
import datetime
import re
from collections import Counter
import requests

# Common words to ignore when finding trends
STOP_WORDS = {
    "the", "a", "an", "in", "on", "at", "to", "of", "and", "or", "is",
    "are", "was", "were", "for", "with", "by", "from", "that", "this",
    "it", "its", "as", "be", "has", "have", "had", "but", "not", "no",
    "he", "she", "they", "we", "you", "i", "my", "his", "her", "their",
    "will", "can", "do", "did", "into", "over", "after", "says", "said",
    "new", "up", "out", "india", "indian",
}


def extract_trends(headlines: list[str], top_n: int = 5) -> list[str]:
    words = []
    for h in headlines:
        tokens = re.findall(r"\b[a-zA-Z]{4,}\b", h.lower())
        words.extend(t for t in tokens if t not in STOP_WORDS)
    counter = Counter(words)
    return [word.title() for word, _ in counter.most_common(top_n)]


def get_news_data() -> dict:
    api_key = os.environ["NEWS_API_KEY"]

    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "in",
        "pageSize": 10,
        "apiKey": api_key,
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    raw = resp.json()

    articles = raw.get("articles", [])
    headlines = []

    for art in articles:
        title = art.get("title") or ""
        if title and "[Removed]" not in title:
            headlines.append({
                "title": title.strip(),
                "source": art.get("source", {}).get("name", "Unknown"),
                "url": art.get("url", "#"),
            })

    trend_keywords = extract_trends([h["title"] for h in headlines])

    return {
        "headlines": headlines,
        "trends": trend_keywords,
        "total": len(headlines),
        "fetched_at": datetime.datetime.now().strftime("%d %b %Y, %I:%M %p IST"),
    }
