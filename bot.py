import feedparser, json, datetime, re
from deep_translator import GoogleTranslator

# Lähteet
SOURCES = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://www.theblock.co/rss"
]

MAX_PER_SOURCE = 3
MAX_TOTAL = 6

def sanitize_title(t):
    t = re.sub(r"[^a-zA-Z0-9äöÄÖ.,:;!?()'\" \-\u00C0-\u017F]", "", t)
    return re.sub(r"\s+", " ", t).strip()

def translate_to_fi(text):
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
                title = sanitize_title(e.get("title", "").strip())
                link = e.get("link", "").strip()
                if not title or not link:
                    continue
                if len(title) > 180:
                    title = title[:177] + "…"
                img = ""
                if "media_content" in e and len(e.media_content) > 0:
                    img = e.media_content[0].get("url", "")
                items.append({"title": title, "link": link, "img": img})
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
            "link": it["link"],
            "img": it.get("img", "")
        })
    return cards

def run():
    entries = fetch_entries()
    today = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = {"date": today, "cards": build_cards(entries)}
    with open("latest.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("✅ latest.json päivitetty")
    build_site(payload)

def build_site(data):
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y klo %H:%M")

    # Luo kortit uutisista
    cards_html = ""
    for c in data.get("cards", []):
        img_html = f'<img src="{c["img"]}" alt="" class="thumb">' if c["img"] else ""
        cards_html += f"""
        <div class="card">
            {img_html}
            <h3><a href="{c['link']}" target="_blank">{c['title']}</a></h3>
            <p>{c['desc']}</p>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="fi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MyCryptoFI — Krypto-opas suomalaisille</title>
<style>
body {{
    margin: 0;
    background: #000814;
    color: #e6f1ff;
    font-family: 'Inter', Arial, sans-serif;
    overflow-x: hidden;
}}
header {{
    padding: 60px 5%;
    text-align: center;
    color: white;
    background: linear-gradient(180deg, #001d3d 0%, #000814 100%);
}}
header h1 {{
    font-size: 2.4rem;
    letter-spacing: -0.02em;
    font-weight: 800;
}}
header p {{
    opacity: 0.85;
    font-size: 1.1rem;
}}
section {{
    max-width: 950px;
    margin: 60px auto;
    padding: 0 20px;
}}
.news-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 28px;
}}
.card {{
    background: #001633;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    transition: all 0.2s ease;
}}
.card:hover {{
    background: #002855;
    transform: translateY(-4px);
}}
.card a {{
    color: #61dafb;
    text-decoration: none;
}}
.card a:hover {{
    text-decoration: underline;
}}
.card .thumb {{
    width: 100%;
    border-radius: 10px;
    margin-bottom: 10px;
}}
footer {{
    text-align: center;
    font-size: 0.9rem;
    color: #adb5bd;
    padding: 50px 20px;
    border-top: 1px solid #002b5c;
    background: #000d1a;
}}
</style>
</head>
<body>

<header>
  <h1>Krypto-opas suomalaisille</h1>
  <p>Ymmärrä digitaalinen talous — ilman hypeä</p>
</header>

<section>
  <h2>📰 Uusimmat kryptouutiset</h2>
  <p style="color:#a8b2d1; font-size:0.9rem;">Päivitetty {timestamp}</p>
  <div class="news-grid">
      {cards_html if cards_html else "<p>Ei uutisia juuri nyt.</p>"}
  </div>
</section>

<footer>
  © 2025 MyCryptoFI — Rakennettu tekoälyllä ja GitHub Actionsilla.
</footer>

</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ Sivusto rakennettu onnistuneesti")

if __name__ == "__main__":
    run()
