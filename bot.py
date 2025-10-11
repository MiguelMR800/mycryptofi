import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

# 🔹 CoinDesk RSS
RSS_FEED = "https://www.coindesk.com/arc/outboundfeeds/rss/"

# 🔹 Tiedostonimet
HTML_FILE = "index.html"
LOG_FILE = "render_style.json"

# 🔹 Tiivistys ja käännös (kevyt)
def summarize_article(title, summary):
    summary = summary.replace("\n", " ").strip()
    if len(summary) > 300:
        summary = summary[:300].rsplit(" ", 1)[0] + "..."
    return f"<b>{title}</b> — {summary}"

# 🔹 Päivitä HTML
def update_html(latest_articles):
    try:
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        html = "<html><body><h2>Crypto News</h2><div id='news'></div></body></html>"

    soup = BeautifulSoup(html, "html.parser")
    news_div = soup.find("div", {"id": "news"})
    if not news_div:
        news_div = soup.new_tag("div", id="news")
        soup.body.append(news_div)

    # Poistetaan vanhat uutiset
    for child in news_div.find_all("div", {"class": "article"}):
        child.decompose()

    # Lisätään uudet
    for article in latest_articles:
        item = soup.new_tag("div", **{"class": "article"})
        item.string = article
        news_div.append(item)

    # Tallenna
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(str(soup))

# 🔹 Hae RSS ja päivitä
def fetch_and_update():
    print(f"[{datetime.now()}] Fetching CoinDesk feed...")
    feed = feedparser.parse(RSS_FEED)
    articles = []
    for entry in feed.entries[:5]:
        title = entry.title
        summary = BeautifulSoup(entry.summary, "html.parser").get_text()
        articles.append(summarize_article(title, summary))
    update_html(articles)
    print(f"[{datetime.now()}] Updated {len(articles)} articles.")

# 🔹 Lokitus
def log_update():
    log = {"last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

# 🔹 Suorita
if __name__ == "__main__":
    fetch_and_update()
    log_update()
    print("✅ CoinDesk news updated successfully.")
