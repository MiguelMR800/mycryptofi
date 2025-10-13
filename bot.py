# MyCryptoFI v3 — täysi sivugeneraattori (uutiset + pörssit + lompakot)
# ---------------------------------------------------------------
# Toimi näin:
# 1) Täytä AFFILIATE_LINKS alla omilla linkeilläsi (tai tee affiliates.json viereen).
# 2) Commit -> Actions -> Run workflow: Fetch crypto news.
# 3) Botti tuottaa index.html:n ja GitHub Pages julkaisee sen.

import feedparser, json, datetime, re, html
from deep_translator import GoogleTranslator

# --- A) KONFIGURAATIO ---------------------------------------------------------

# Täytä omat affiliate-linkkisi tähän (tai tee viereen affiliates.json ja jätä nämä ennalleen)
AFFILIATE_LINKS = {
    # Pörssit
    "binance":  "https://accounts.binance.com/register?ref=YOUR_CODE",
    "bybit":    "https://www.bybit.com/invite?ref=YOUR_CODE",
    "bitget":   "https://www.bitget.com/en/register?from=referral&clacCode=YOUR_CODE",
    "mexc":     "https://www.mexc.com/register?inviteCode=YOUR_CODE",
    "cryptocom":"https://crypto.com/app/YOUR_CODE",

    # Suomipalvelut
    "coinmotion":  "https://coinmotion.com/fi?ref=YOUR_CODE",
    "northcrypto": "https://northcrypto.com/fi/register?ref=YOUR_CODE",

    # Kylmälompakot
    "ledger":  "https://shop.ledger.com/?r=YOUR_CODE",
    "trezor":  "https://trezor.io?offer_id=YOUR_CODE",
}

# Jos viereen on lisätty affiliates.json (avaimet samat kuin yllä), se yliajaa yllä olevan dictin.
def load_affiliates():
    try:
        with open("affiliates.json", "r", encoding="utf-8") as f:
            ext = json.load(f)
            if isinstance(ext, dict):
                AFFILIATE_LINKS.update(ext)
    except Exception:
        pass

# RSS-lähteet (engl.)
SOURCES = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://www.theblock.co/rss"
]

MAX_PER_SOURCE = 3     # max/kanava
MAX_TOTAL = 6          # max yhteensä etusivulle

# --- B) APUFUNKTIOT -----------------------------------------------------------

def sanitize_title(t: str) -> str:
    t = re.sub(r"[^a-zA-Z0-9äöÄÖ.,:;!?()'\" \-\u00C0-\u017F]", "", t)
    return re.sub(r"\s+", " ", t).strip()

def translate_to_fi(text: str) -> str:
    """Käännä suomeksi, fallback alkuperäiseen jos jotain tapahtuu."""
    try:
        out = GoogleTranslator(source="auto", target="fi").translate(text)
        return out if out else text
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

                # Kuva: media_content / image-tyyppiset linkit
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
                if len(title) > 200:
                    title = title[:197] + "…"

                items.append({"title": title, "link": link, "img": img})
        except Exception:
            continue
    return items

def build_news_cards(entries):
    """Muodosta uutiskortit (otsikko käännettynä suomeksi, CTA-nappi)."""
    html_cards = ""
    for it in entries[:MAX_TOTAL]:
        fi_title = html.escape(translate_to_fi(it["title"]))
        img_tag = f'<img src="{html.escape(it["img"])}" alt="" loading="lazy">' if it["img"] else ""
        html_cards += f"""
        <article class="card">
            {img_tag}
            <h3>{fi_title}</h3>
            <a class="btn" href="{html.escape(it['link'])}" target="_blank" rel="noopener noreferrer">Lue artikkeli</a>
        </article>
        """
    return html_cards

def affiliate_section():
    """Pörssit + lompakot esittelyineen (lyhyet, konversion kannalta selkeät kuvaukset)."""
    A = AFFILIATE_LINKS  # shorthand

    items = [
        # Pörssit
        {
            "title": "Binance",
            "desc": "Maailman suurin pörssi. Nopeat siirrot, matalat kulut, laaja tarjonta.",
            "href": A.get("binance", "#")
        },
        {
            "title": "Bybit",
            "desc": "Johdannaiset, spot, copy trading. Suosittu treidaajille.",
            "href": A.get("bybit", "#")
        },
        {
            "title": "Bitget",
            "desc": "Aktiivitreidaajille. Laaja valikoima ja kilpailukykyiset kulut.",
            "href": A.get("bitget", "#")
        },
        {
            "title": "MEXC",
            "desc": "Uusia listauksia usein. Hyvä altcoin-screenerin kanssa.",
            "href": A.get("mexc", "#")
        },
        {
            "title": "Crypto.com",
            "desc": "Pörssi + kortti. Helppo arjen käyttöön.",
            "href": A.get("cryptocom", "#")
        },

        # Suomipalvelut
        {
            "title": "Coinmotion (FI)",
            "desc": "Kotimainen toimija, verot ja raportointi helppoja.",
            "href": A.get("coinmotion", "#")
        },
        {
            "title": "Northcrypto (FI)",
            "desc": "Kotimainen palvelu, selkeä käyttöliittymä.",
            "href": A.get("northcrypto", "#")
        },

        # Kylmälompakot
        {
            "title": "Ledger",
            "desc": "Turvallinen kylmälompakko — suojaa varasi offline.",
            "href": A.get("ledger", "#")
        },
        {
            "title": "Trezor",
            "desc": "Avoimen lähdekoodin hardware-lompakko — helppo käyttää.",
            "href": A.get("trezor", "#")
        },
    ]

    cards = ""
    for it in items:
        title = html.escape(it["title"])
        desc = html.escape(it["desc"])
        href = html.escape(it["href"])
        cards += f"""
        <div class="aff-card">
            <h4>{title}</h4>
            <p>{desc}</p>
            <a class="btn" href="{href}" target="_blank" rel="noopener noreferrer">Avaa →</a>
        </div>
        """
    return f"""
    <section class="affiliates" id="palvelut">
      <h2>📊 Suositellut pörssit & lompakot</h2>
      <p class="muted">Valitut palvelut: helppokäyttöisyys, likviditeetti ja turvallisuus.</p>
      <div class="aff-grid">
        {cards}
      </div>
    </section>
    """

# --- C) SIVUNRAKENNUS ---------------------------------------------------------

def build_site():
    load_affiliates()  # lataa affiliates.json jos löytyy

    entries = fetch_entries()
    today = datetime.datetime.now().strftime("%d.%m.%Y klo %H:%M")
    cards_html = build_news_cards(entries)
    affiliate_html = affiliate_section()

    html_out = f"""<!doctype html>
<html lang="fi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>MyCryptoFI — Krypto-opas suomalaisille</title>
  <meta name="description" content="Suomalainen krypto-opas: uutiset, pörssit, lompakot ja käytännön vinkit ilman hypeä.">
  <style>
    :root {{
      --bg: #000814;
      --bg-grad: radial-gradient(1200px 600px at 50% -10%, #002952 0%, #001a33 35%, #000814 70%);
      --card: #001f3f;
      --accent: #61dafb;
      --accent-2: #0077ff;
      --muted: #a8b2d1;
      --border: #003260;
      --text: #e6f1ff;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin:0; padding:0; background:var(--bg); color:var(--text); font-family: Inter, system-ui, -apple-system, Segoe UI, Arial, sans-serif; }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .wrap {{ max-width: 1200px; padding: 0 24px; margin: 0 auto; }}

    header {{
      background: var(--bg-grad);
      padding: 96px 0 40px;
      text-align: center;
    }}
    header h1 {{ font-size: clamp(2rem, 5vw, 3rem); margin:0 0 8px; letter-spacing:-0.02em; font-weight:800; }}
    header p  {{ color: var(--muted); margin:0; font-size: clamp(1rem, 2.5vw, 1.25rem); }}

    section {{ padding: 48px 0; }}
    h2 {{ font-size: clamp(1.4rem, 2.5vw, 1.8rem); margin: 0 0 8px; text-align:center; }}
    .muted {{ color: var(--muted); text-align:center; margin:0 0 24px; }}

    /* News grid */
    .grid {{
      display:grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 24px;
    }}
    .card {{
      background: var(--card);
      border-radius: 16px;
      border: 1px solid var(--border);
      box-shadow: 0 8px 24px rgba(0,0,0,0.25);
      overflow:hidden;
      transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
    }}
    .card:hover {{
      transform: translateY(-4px);
      border-color: var(--accent-2);
      box-shadow: 0 12px 28px rgba(0, 119, 255, 0.25);
    }}
    .card img {{
      width:100%; height:170px; object-fit:cover; display:block; border-bottom:1px solid var(--border);
      background:#00213f;
    }}
    .card h3 {{ padding: 14px 16px 6px; margin:0; font-size:1rem; color:var(--accent); }}
    .card .btn {{
      margin: 8px 16px 18px;
      display:inline-block;
      background: var(--accent-2);
      color: #fff;
      padding: 8px 14px;
      border-radius: 10px;
      text-decoration:none;
      font-weight:700;
    }}
    .card .btn:hover {{ background:#3399ff; }}

    /* Affiliates */
    .affiliates {{ background: #000d1a; border-top:1px solid var(--border); }}
    .aff-grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; }}
    .aff-card {{
      background:#001a33; border:1px solid var(--border); border-radius:14px; padding:16px; text-align:left;
      transition: transform .2s, box-shadow .2s, border-color .2s;
    }}
    .aff-card:hover {{ transform: translateY(-4px); border-color: var(--accent-2); box-shadow: 0 12px 28px rgba(0, 119, 255, 0.22); }}
    .aff-card h4 {{ margin:0 0 6px; color:var(--accent); }}
    .aff-card p {{ margin:0 0 10px; color:var(--muted); font-size:0.95rem; line-height:1.35rem; }}
    .aff-card .btn {{ background: var(--accent-2); color:#fff; padding:7px 12px; border-radius:10px; display:inline-block; font-weight:700; }}
    .aff-card .btn:hover {{ background:#3399ff; }}

    footer {{
      padding: 28px 0 40px; text-align:center; color:var(--muted); border-top:1px solid var(--border);
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <h1>Krypto-opas suomalaisille</h1>
      <p>Ymmärrä digitaalinen talous — ilman hypeä</p>
    </div>
  </header>

  <main class="wrap">
    <section id="uutiset">
      <h2>📰 Uusimmat kryptouutiset</h2>
      <p class="muted">Päivitetty {today}</p>
      <div class="grid">
        {cards_html if cards_html.strip() else '<p class="muted">Ei uutisia juuri nyt.</p>'}
      </div>
    </section>
  </main>

  {affiliate_html}

  <footer>
    <div class="wrap">
      © 2025 MyCryptoFI — Rakennettu automaatiolla (GitHub Actions).
    </div>
  </footer>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_out)

# --- D) AJOKOMENTO ------------------------------------------------------------

if __name__ == "__main__":
    build_site()
