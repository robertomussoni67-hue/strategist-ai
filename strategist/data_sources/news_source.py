# news_source.py
import feedparser

# Elenco feed RSS da cui prendere le notizie
FEEDS = [
    "http://feeds.reuters.com/reuters/businessNews",
    "https://www.ilsole24ore.com/rss/notizie_mondo.xml"
]

def get_latest_news(n=3):
    """
    Restituisce un dizionario {fonte: [lista titoli]} con le ultime n notizie.
    """
    notizie = {}
    for url in FEEDS:
        try:
            parsed = feedparser.parse(url)
            if parsed.entries:
                notizie[url] = [entry.title for entry in parsed.entries[:n]]
        except Exception as e:
            print(f"Errore news_source: {e}")
    return notizie

# Test veloce
if __name__ == "__main__":
    news = get_latest_news()
    for fonte, titoli in news.items():
        print(f"--- News da {fonte} ---")
        for titolo in titoli:
            print(f"- {titolo}")