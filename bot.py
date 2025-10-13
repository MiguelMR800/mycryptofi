import feedparser, json, datetime, os, re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SOURCES = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://www.theblock.co/rss"
]

MAX_TOTAL = 6

def clean(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def fetch_news():
    all_items = []
    for src in SOURCES:
        feed = feedparser.parse(src)
        for entry in feed.entries[:3]:
            title = clean(entry.get("title", ""))
            link = entry.get("link", "")
            image = ""
            if "media_content" in entry and len(entry.media_content) > 0:
                image = entry.media_content[0].get("url", "")
            elif "links" in entry:
                for l in entry.links:
                    if "image" in l.get("type", ""):
                        image = l.get("href", "")
            if title and link:
                all_items.append({"title": title, "link": link, "image": image})
    return all_items[:MAX_TOTAL]

def translate_and_summarize(title):
    prompt = f"""
Käännä seuraava kryptouutisen otsikko suomeksi ja tee 1–2 virkkeen ytimekäs tiivistelmä suomeksi.

Otsikko:
{title}

Palauta täsmälleen JSON-muodossa:
{{"title_fi": "...", "summary_fi": "..."}}
"""
    try:
        r = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=200
        )
        txt = r.choices[0].message.content.strip()
        match = re.search(r"\{.*\}", txt, re.S)
        if match:
            data = json.loads(match.group(0))
            return data.get("title_fi", title), data.get("summary_fi", "")
        else:
            return title, ""
    except Exception as e:
        print("⚠️ Virhe käännöksessä:", e)
        return title, ""

def main():
    print("🔄 Haetaan kryptouutisia...")
    news = fetch_news()
    cards = []
    for n in news:
        print("📰 Käännetään:", n["title"])
        fi_title, fi_summary = translate_and_summarize(n["title"])
        cards.append({
            "title": fi_title,
            "summary": fi_summary,
            "image": n["image"],
            "link": n["link"]
        })
    result = {"date": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "cards": cards}
    with open("latest.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("✅ Tallennettu latest.json")

if __name__ == "__main__":
    main()
