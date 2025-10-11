import feedparser, random, json, datetime, re
sources=[
 "https://www.coindesk.com/arc/outboundfeeds/rss/",
 "https://cointelegraph.com/rss",
 "https://www.theblock.co/rss"
]
def get_articles():
    arts=[]
    for src in sources:
        d=feedparser.parse(src)
        for e in d.entries[:3]:
            if len(e.title)<150:
                arts.append((e.title,e.link))
    return arts
def summarize(txt):
    txt=re.sub(r"[^a-zA-Z0-9äöÄÖ., ]","",txt)
    return txt.split(":")[0].strip()
def run():
    arts=get_articles()
    today=datetime.datetime.now().strftime("%Y-%m-%d")
    newcards=[]
    for t,l in arts[:3]:
        newcards.append({"title":summarize(t),"desc":"Lähde: "+l})
    with open("latest.json","w",encoding="utf-8") as f:
        json.dump({"date":today,"cards":newcards},f,ensure_ascii=False,indent=2)
if __name__=="__main__":
    run()
