import json, os, urllib.request, urllib.parse, datetime
import xml.etree.ElementTree as ET

CH = "UC9ZuLxKplI6AmLSDWRm-JVg"
KEY = os.environ.get("YT_API_KEY", "").strip()
NS = {"a": "http://www.w3.org/2005/Atom", "m": "http://search.yahoo.com/mrss/"}
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 reshay-stats"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def load(name, default):
    try:
        return json.load(open(name, encoding="utf-8"))
    except Exception:
        return default


videos = {}
root = ET.fromstring(get(f"https://www.youtube.com/feeds/videos.xml?channel_id={CH}"))
for e in root.findall("a:entry", NS):
    vid = e.find("{http://www.youtube.com/xml/schemas/2015}videoId").text
    g = e.find("m:group", NS)
    st = g.find("m:community/m:statistics", NS)
    rt = g.find("m:community/m:starRating", NS)
    videos[vid] = {
        "id": vid,
        "title": e.find("a:title", NS).text,
        "published": e.find("a:published", NS).text,
        "views": int(st.get("views")) if st is not None else 0,
        "likes": int(rt.get("count")) if rt is not None else 0,
        "comments": None,
    }

subs = None
if KEY and videos:
    ids = ",".join(videos)
    q = urllib.parse.urlencode({"part": "statistics", "id": ids, "key": KEY})
    for it in json.loads(get("https://www.googleapis.com/youtube/v3/videos?" + q))["items"]:
        s = it["statistics"]
        v = videos[it["id"]]
        v["views"] = int(s.get("viewCount", v["views"]))
        v["likes"] = int(s.get("likeCount", v["likes"]))
        v["comments"] = int(s.get("commentCount", 0))
    q = urllib.parse.urlencode({"part": "statistics", "id": CH, "key": KEY})
    subs = int(json.loads(get("https://www.googleapis.com/youtube/v3/channels?" + q))["items"][0]["statistics"].get("subscriberCount", 0))

rows = sorted(videos.values(), key=lambda v: v["published"])
prev = load("latest.json", {})
latest = {"updated": now, "subscribers": subs if subs is not None else prev.get("subscribers"), "videos": rows}
json.dump(latest, open("latest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

hist = load("history.json", [])
for v in rows:
    hist.append({"ts": now, "platform": "YouTube", "id": v["id"], "title": v["title"], "views": v["views"], "likes": v["likes"], "comments": v["comments"]})
json.dump(hist[-5000:], open("history.json", "w", encoding="utf-8"), ensure_ascii=False)
print("ok", len(rows), "videos")
