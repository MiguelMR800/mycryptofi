#!/usr/bin/env python3
import os, re, json, time, datetime, html, sys
from urllib.parse import urlparse

SITE_TITLE = "MyCryptoFI"
BASE_URL = "https://mycryptofi.com"  # jos Pages julkaisussa eri polku, muuta tämä
RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://decrypt.co/feed",
]
MAX_ARTICLES = 6
ART_DIR = "articles"
NEWS_JSON = "news.json"
INDEX_HTML = "index.html"
ARTICLE_TEMPLATE = "article_template.html"

def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:120] or "artikkeli"

def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def translate_fi(text):
    text = text or ""
    try:
        from deep_translator import GoogleTranslator
        if len(text) < 4500:
            return GoogleTranslator(source="auto", target="fi").translate(text)
        parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
        out = []
        for p in parts:
            out.append(GoogleTranslator(source="auto", target="fi").translate(p))
            time.sleep(0.5)
        return "".join(out)
    except Exception:
        return text

def fetch_feeds(urls):
    try:
        import feedparser
    except ImportError:
        print("feedparser puuttuu", file=sys.stderr)
        return []
    items = []
    for url in urls:
        feed = feedparser.parse(url)
        for e in feed.entries[:10]:
            items.append({
                "title": getattr(e, "title", "(no title)"),
                "link": getattr(e, "link", ""),
                "summary": html.unescape(getattr(e, "summary", "")),
                "published": getattr(e, "published", ""),
                "source": urlparse(url).hostname or "feed",
            })
    # deduplikointi linkin perusteella
    seen=set(); uniq=[]
    for it in items:
        if it["link"] in seen: 
            continue
        seen.add(it["link"]); 
        uniq.append(it)
    return uniq

def render_article(template, data):
    html_out = template
    for k,v in data.items():
        html_out = html_out.replace(f"{{{{{k}}}}}", str(v))
    return html_out

def build():
    template = read_file(ARTICLE_TEMPLATE)
    items = fetch_feeds(RSS_FEEDS)

    articles = []
    for it in items[:MAX_ARTICLES*2]:  # haetaan enemmän kuin näytetään, varmuusvaralla
        title_fi = translate_fi(it["title"])
        # siistitään summary: poistetaan html-tagit ja käännetään
        clean_summary = re.sub("<[^<]+?>", "", it["summary"] or "").strip()
        summary_fi = translate_fi(clean_summary)
        slug = slugify(title_fi or it["title"])
        file_name = f"{slug}.html"
        art_path = os.path.join(ART_DIR, file_name)

        meta = {
            "title": (title_fi or it["title"]).strip(),
            "summary": (summary_fi or clean_summary).strip(),
            "source": it["source"],
            "source_url": it["link"],
            "published": it["published"] or now_iso(),
            "url": f"{BASE_URL}/{ART_DIR}/{file_name}",
            "slug": slug,
        }

        # artikkelisivu
        article_html = render_article(template, {
            "SITE_TITLE": SITE_TITLE,
            "TITLE": html.escape(meta["title"]),
            "SUMMARY": html.escape(meta["summary"]),
            "PUBLISHED": html.escape(meta["published"]),
            "SOURCE": html.escape(meta["source"]),
            "SOURCE_URL": html.escape(meta["source_url"]),
        })
        write_file(art_path, article_html)
        articles.append(meta)

    # rajataan etusivulle
    articles = articles[:MAX_ARTICLES]

    # news.json
    write_file(NEWS_JSON, json.dumps({"generated_at": now_iso(), "articles": articles}, ensure_ascii=False, indent=2))

    # index.html uutiskorttien korvaus
    if os.path.exists(INDEX_HTML):
        idx = read_file(INDEX_HTML)
        cards = []
        for a in articles:
            cards.append(f'''<a class="card" href="/{ART_DIR}/{a["slug"]}.html">
  <h3>{html.escape(a["title"])}</h3>
  <p class="muted">{html.escape(a["published"])} — {html.escape(a["source"])}</p>
  <p>{html.escape(a["summary"][:180])}…</p>
</a>''')
        news_html = "\n".join(cards) if cards else "<p class=\"muted\">Ei uutisia juuri nyt.</p>"
        import re as _re
        idx = _re.sub(r"<!-- NEWS_START -->(.*?)<!-- NEWS_END -->",
                      f"<!-- NEWS_START -->\n<div class=\"news-grid\">{news_html}\n</div>\n<!-- NEWS_END -->",
                      idx, flags=_re.S)
        write_file(INDEX_HTML, idx)

    print(f"OK. Generoitu {len(articles)} artikkelia.")

if __name__ == "__main__":
    build()
