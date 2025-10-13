import feedparser, json, datetime, re, time
from deep_translator import GoogleTranslator

SOURCES = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://www.theblock.co/rss"
]

MAX_PER_SOURCE = 3        # montako uutista per lähde
MAX_TOTAL = 6             # montako uutista yhteensä (uutislistassa)

def sanitize_title(t: str) -> str:
    t = re.sub(r"[^a-zA-Z0-9äöÄÖ.,:;!?()'\" \-\u00C0-\u017F]", "", t)
    return re.sub(r"\s+", " ", t).strip()

def translate_to_fi(text: str) -> str:
    try:
        return GoogleTranslator(source="auto", target="fi").translate(text)
    except Exception:
        return text

def fetch_entries():
    items = []
    for src in SOURCES:
        try:
            d = feedparser.parse(src)
            for e in d.entries[:MAX_PER_SOURCE]:
                title = e.get("title", "").strip()
                link = e.get("link", "").strip()
                if not title or not link:
                    continue
                title = sanitize_title(title)
                if len(title) > 180:
                    title = title[:177] + "…"
                items.append({"title": title, "link": link})
        except Exception:
            continue
    return items

def build_cards(entries):
    cards = []
    for it in entries[:MAX_TOTAL]:
        fi_title = translate_to_fi(it["title"])
        cards.append({
            "title": fi_title,
            "desc": f"Lähde: {it['link']}",
            "link": it["link"]
        })
    return cards

def run():
    entries = fetch_entries()
    today = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = {
        "date": today,
        "cards": build_cards(entries)
    }
    with open("latest.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print("✅ latest.json luotu onnistuneesti!")
    build_html()  # Rakenna sivu samalla


# ---------------------------
# HTML-generointi alkaa tästä
# ---------------------------

def build_html():
    try:
        with open("latest.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ latest.json puuttuu, ei voida rakentaa HTML:ää.")
        return

    articles_html = ""
    for item in data.get("cards", []):
        title = item.get("title", "Untitled")
        desc = item.get("desc", "")
        link = item.get("link", "#")
        articles_html += f"""
        <div class="news-card">
            <h3><a href="{link}" target="_blank">{title}</a></h3>
            <p>{desc}</p>
        </div>
        """

    timestamp = datetime.datetime.now().strftime("%d.%m.%Y klo %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="fi">
<head>
    <meta charset="UTF-8">
    <title>Uusimmat kryptouutiset - MyCryptoFI</title>
    <link rel="stylesheet" href="style.css">
    <style>
        body {{
            background-color: #0a192f;
            color: #e6f1ff;
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: auto;
            padding: 40px;
        }}
        a {{
            color: #64ffda;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .news-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 20px;
            transition: all 0.2s ease-in-out;
        }}
        .news-card:hover {{
            background: rgba(255,255,255,0.1);
        }}
        footer {{
            text-align: center;
            margin-top: 40px;
            opacity: 0.7;
        }}
    </style>
</head>
<body>
    <h1>📰 Uusimmat kryptouutiset</h1>
    <p><i>Päivitetty {timestamp}</i></p>
    <div class="news-container">
        {articles_html if articles_html else "<p>Ei uutisia saatavilla juuri nyt.</p>"}
    </div>
    <footer>
        <p>© 2025 MyCryptoFI — Rakennettu automaattisesti GitHub Actionsilla.</p>
    </footer>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html päivitetty onnistuneesti!")


# ---------------------------
# Käynnistys
# ---------------------------

if __name__ == "__main__":
    run()
