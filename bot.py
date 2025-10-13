import feedparser, json, datetime, re
from deep_translator import GoogleTranslator

SOURCES = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://www.theblock.co/rss"
]

MAX_PER_SOURCE = 3
MAX_TOTAL = 6

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
                img = ""
                if "media_content" in e and e.media_content:
                    img = e.media_content[0].get("url", "")
                elif "links" in e:
                    for l in e.links:
                        if l.get("type", "").startswith("image"):
                            img = l.get("href", "")
                            break
                if not title or not link:
                    continue
                title = sanitize_title(title)
                if len(title) > 180:
                    title = title[:177] + "…"
                items.append({"title": title, "link": link, "img": img})
        except Exception:
            continue
    return items

def build_cards(entries):
    html = ""
    for it in entries[:MAX_TOTAL]:
        fi_title = translate_to_fi(it["title"])
        img_tag = f'<img src="{it["img"]}" alt="news">' if it["img"] else ""
        html += f"""
        <div class="card">
            {img_tag}
            <h3>{fi_title}</h3>
            <p>Lähde:<br>{it["link"]}</p>
        </div>
        """
    return html

def build_site():
    entries = fetch_entries()
    today = datetime.datetime.utcnow().strftime("%d.%m.%Y klo %H:%M")
    cards_html = build_cards(entries)

    html = f"""<!DOCTYPE html>
<html lang="fi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MyCryptoFI — Krypto-opas suomalaisille</title>
  <style>
    body {{
      margin: 0;
      font-family: 'Inter', Arial, sans-serif;
      background: radial-gradient(circle at top, #001a33, #000814 70%);
      color: white;
      text-align: center;
    }}
    header {{
      padding: 100px 20px 50px;
    }}
    h1 {{
      font-size: 2.4rem;
      font-weight: 700;
      margin-bottom: 10px;
    }}
    h2 {{
      color: #b8d8ff;
      margin-bottom: 30px;
    }}
    section {{
      padding: 20px;
      max-width: 1200px;
      margin: auto;
    }}
    .cards {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 25px;
      justify-items: center;
    }}
    .card {{
      background: #001f3f;
      border-radius: 16px;
      box-shadow: 0 0 20px rgba(0,0,0,0.3);
      overflow: hidden;
      transition: transform 0.3s, box-shadow 0.3s;
      width: 100%;
      max-width: 360px;
    }}
    .card:hover {{
      transform: translateY(-6px);
      box-shadow: 0 0 25px rgba(0,122,255,0.5);
    }}
    .card img {{
      width: 100%;
      height: 180px;
      object-fit: cover;
      border-bottom: 3px solid #0077ff;
    }}
    .card h3 {{
      color: #61dafb;
      font-size: 1.05rem;
      padding: 14px;
    }}
    .card p {{
      color: #ccc;
      font-size: 0.85rem;
      padding: 0 14px 20px;
      word-wrap: break-word;
    }}
    footer {{
      text-align: center;
      padding: 60px 20px;
      background: #000d1a;
      border-top: 1px solid #002b5c;
    }}
    footer .partners {{
      margin-bottom: 14px;
    }}
    footer .partners a {{
      display: inline-block;
      margin: 6px 10px;
      color: #61dafb;
      font-weight: 600;
      text-decoration: none;
      background: rgba(0, 50, 100, 0.4);
      padding: 8px 16px;
      border-radius: 12px;
      transition: all 0.2s ease;
    }}
    footer .partners a:hover {{
      background: #0077ff;
      color: #fff;
    }}
    footer p {{
      color: #adb5bd;
      font-size: 0.9rem;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Krypto-opas suomalaisille</h1>
    <h2>Ymmärrä digitaalinen talous — ilman hypeä</h2>
  </header>
  <section>
    <h3>📰 Uusimmat kryptouutiset</h3>
    <p>Päivitetty {today}</p>
    <div class="cards">{cards_html}</div>
  </section>
  <footer>
    <div class="partners">
      <a href="https://accounts.binance.com/register?ref=AFFIKOODI" target="_blank">Binance</a>
      <a href="https://www.bybit.com/invite?ref=AFFIKOODI" target="_blank">Bybit</a>
      <a href="https://www.mexc.com/register?inviteCode=AFFIKOODI" target="_blank">MEXC</a>
      <a href="https://www.crypto.com/app/AFFIKOODI" target="_blank">Crypto.com</a>
      <a href="https://shop.ledger.com/?r=AFFIKOODI" target="_blank">Ledger</a>
      <a href="https://trezor.io?offer_id=AFFIKOODI" target="_blank">Trezor</a>
    </div>
    <p>© 2025 MyCryptoFI — Ymmärrä digitaalinen talous ilman hypeä.</p>
  </footer>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    build_site()
