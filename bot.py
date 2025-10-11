import feedparser, json

feeds = [
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("Decrypt", "https://decrypt.co/feed"),
    ("Cointelegraph", "https://cointelegraph.com/rss")
]

articles = []
for name, url in feeds:
    feed = feedparser.parse(url)
    for entry in feed.entries[:3]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "source": name
        })

with open("news.json", "w", encoding="utf-8") as f:
    json.dump({"articles": articles}, f, indent=2, ensure_ascii=False)

print("✅ Uutiset päivitetty news.json-tiedostoon.")
