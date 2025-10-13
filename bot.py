import feedparser, json, datetime, re, os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SOURCES = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://www.theblock.co/rss"
]

MAX_PER_SOURCE = 3
MAX_TOTAL = 6

def sanitize_text(t: str) -> str:
    t = re.sub(r"[^a-zA-Z0-9äöÄÖ.,:;!?()'\" \-\u00C0-\u017F]", "", t)
    return re.sub(r"\s+", " ", t).strip()

def fetch_entries():
    items = []
    for src in SOURCES:
        try:
            d = feedparser.parse(src)
            for e in d.entries[:MAX_PER_SOURCE]:
                title = e.get("title", "").strip()
                link = e.get("link", "").strip()
                image = e.get("media_content", [{}])[0].get("url", "")
                if not title or not link:
                    continue
                title = sanitize_text(title)
                if len(title) > 180:
                    title = title[:177] + "…"
                items.append({
                    "title": title,
                    "link": link,
                    "image": image
                })
        except Exception as ex:
            print(f"Error reading {src}: {ex}")
    return items[:MAX_TOTAL]

def translate_and_summarize(text: str) -> dict:
    """Kääntää ja tiivistää suomeksi OpenAI:n avulla."""
    try:
        prompt = f"""
        Käännä seuraava englanninkielinen kryptouutisen otsikko suomeksi
        ja tee 1–2 virkkeen tiivistelmä, joka kuulostaa luonnolliselta uutistekstiltä.

        Otsikko: "{text}"
        Palauta tulos muodossa:
        otsikko: <suomennettu otsikko>
        tiivistelmä: <lyhyt suomenkielinen tiivistelmä>
        """
        resp = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=180
        )
        answer = resp.choices[0].message.content
        parts = re.findall(r"otsikko:\s*(.*)\ntiivistelmä:\s*(.*)", answer, re.IGNORECASE)
        if parts:
            return {"title": parts[0][0].strip(), "summary": parts[0][1].strip()}
        else:
            return {"title": text, "summary": ""}
    except Exception as ex:
        print(f"Translation error: {ex}")
        return {"title": text, "summary": ""}

def build_cards(entries):
    cards = []
    for it in entries:
        translated = translate_and_summarize(it["title"])
        cards.append({
            "title": translated["title"],
            "summary": translated["summary"],
            "image": it.get("image", ""),
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
    print("✅ latest.json päivitetty onnistuneesti.")

if __name__ == "__main__":
    run()
