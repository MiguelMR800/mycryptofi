import os
import json
import datetime
import feedparser
import re
from openai import OpenAI

# Luo OpenAI-asiakas (käyttää GitHubin secretistä asetettua avainta)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# RSS-lähteet
SOURCES = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://www.theblock.co/rss"
]

# Kuinka monta uutista per lähde ja yhteensä
MAX_PER_SOURCE = 3
MAX_TOTAL = 6


# --- Apufunktiot ---

def sanitize_text(t: str) -> str:
    """Poistaa erikoismerkit ja ylimääräiset välit."""
    t = re.sub(r"[^a-zA-Z0-9äöÄÖ.,:;!?()'\" \-\u00C0-\u017F]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def translate_and_summarize(text: str) -> tuple[str, str]:
    """Kääntää otsikon suomeksi ja tekee 2–3 lauseen tiivistelmän."""
    try:
        prompt = f"""
Käännä seuraava kryptouutisen otsikko suomeksi ja tee siitä 2–3 lauseen tiivistelmä suomen kielellä.
Pidä tyyli selkeänä, luonnollisena ja suomalaiselle lukijalle sopivana.
Palauta tulos muodossa:

OTSikko: ...
TIIVISTELMÄ: ...
---
{text}
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Olet kokenut talous- ja kryptouutisten kääntäjä."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=180,
            temperature=0.7
        )
        out = response.choices[0].message.content.strip()

        # Erotellaan otsikko ja tiivistelmä
        lines = out.splitlines()
        title = ""
        summary = ""
        for line in lines:
            if line.lower().startswith("otsikko"):
                title = line.split(":", 1)[1].strip()
            elif line.lower().startswith("tiivistelmä"):
                summary = line.split(":", 1)[1].strip()

        return title or text, summary or ""
    except Exception:
        return text, ""


def fetch_entries():
    """Hakee uutiset RSS-lähteistä."""
    items = []
    for src in SOURCES:
        try:
            d = feedparser.parse(src)
            for e in d.entries[:MAX_PER_SOURCE]:
                title = e.get("title", "").strip()
                link = e.get("link", "").strip()
                image = ""
                # Joissain RSS:issä on kuvakenttä
                if "media_content" in e and len(e.media_content) > 0:
                    image = e.media_content[0].get("url", "")
                elif "links" in e:
                    for l in e.links:
                        if "image" in l.get("type", ""):
                            image = l.get("href", "")
                if not title or not link:
                    continue
                title = sanitize_text(title)
                items.append({"title": title, "link": link, "image": image})
        except Exception:
            continue
    return items


def build_cards(entries):
    """Rakentaa käännöksen ja tiivistelmän jokaiselle uutiselle."""
    cards = []
    for it in entries[:MAX_TOTAL]:
        fi_title, fi_summary = translate_and_summarize(it["title"])
        cards.append({
            "title": fi_title,
            "summary": fi_summary,
            "image": it.get("image", ""),
            "link": it["link"]
        })
    return cards


def run():
    """Pääsuoritus: hakee, kääntää ja tallentaa uutiset."""
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
