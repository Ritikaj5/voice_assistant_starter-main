import feedparser

DEFAULT_FEEDS = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://www.reutersagency.com/feed/?best-topics=top-news&post_type=best",
    "https://www.apnews.com/apf-topnews?utm_source=rss"
]

def get_headlines(limit: int = 5):
    headlines = []
    for url in DEFAULT_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit]:
                headlines.append({
                    "title": entry.get("title", "").strip(),
                    "link": entry.get("link", ""),
                    "source": feed.feed.get("title", "News")
                })
        except Exception:
            continue
    # De-duplicate by title while preserving order
    seen = set()
    uniq = []
    for h in headlines:
        if h["title"] in seen:
            continue
        uniq.append(h)
        seen.add(h["title"])
        if len(uniq) >= limit:
            break
    return uniq
