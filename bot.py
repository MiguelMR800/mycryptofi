import feedparser, json, datetime, re, time
from deep_translator import GoogleTranslator

SOURCES = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://www.theblock.co/rss"
]

MAX_PER_SOURCE = 3        # how many items to pull per source
MAX_TOTAL = 6             # cap total items written to latest.json

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
            "desc": f"Lähde: {it['link']}"
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

if __name__ == "__main__":
    run()
