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


CID = os.environ.get("YT_CLIENT_ID", "").strip()
CSEC = os.environ.get("YT_CLIENT_SECRET", "").strip()
RTOK = os.environ.get("YT_REFRESH_TOKEN", "").strip()
analytics = {"updated": now, "error": None}
if CID and CSEC and RTOK:
    try:
        body = urllib.parse.urlencode({"client_id": CID, "client_secret": CSEC, "refresh_token": RTOK, "grant_type": "refresh_token"}).encode()
        tok = json.loads(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=body), timeout=30).read())["access_token"]

        def api(url):
            req = urllib.request.Request(url, headers={"Authorization": "Bearer " + tok})
            return json.loads(urllib.request.urlopen(req, timeout=30).read())

        if videos:
            ids = ",".join(videos)
            for it in api("https://www.googleapis.com/youtube/v3/videos?" + urllib.parse.urlencode({"part": "statistics", "id": ids}))["items"]:
                s = it["statistics"]; v = videos[it["id"]]
                v["views"] = int(s.get("viewCount", v["views"])); v["likes"] = int(s.get("likeCount", v["likes"])); v["comments"] = int(s.get("commentCount", 0))
        ch = api("https://www.googleapis.com/youtube/v3/channels?" + urllib.parse.urlencode({"part": "statistics", "mine": "true"}))["items"][0]["statistics"]
        subs = int(ch.get("subscriberCount", 0))
        start = min([v["published"][:10] for v in videos.values()] or [now[:10]])
        end = now[:10]

        def rep(metrics, dims, extra=None):
            q = {"ids": "channel==MINE", "startDate": start, "endDate": end, "metrics": metrics, "dimensions": dims}
            q.update(extra or {})
            r = api("https://youtubeanalytics.googleapis.com/v2/reports?" + urllib.parse.urlencode(q))
            names = [c["name"] for c in r.get("columnHeaders", [])]
            return [dict(zip(names, row)) for row in r.get("rows", [])]

        analytics["daily"] = rep("views,estimatedMinutesWatched,subscribersGained,likes,comments", "day", {"sort": "day"})
        analytics["videos"] = rep("views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments", "video", {"sort": "-views", "maxResults": "50"})
        analytics["traffic"] = rep("views", "insightTrafficSourceType", {"sort": "-views"})
        analytics["countries"] = rep("views", "country", {"sort": "-views", "maxResults": "10"})
        analytics["totals"] = {"start": start, "end": end}
    except Exception as e:
        analytics["error"] = repr(e)[:300]
else:
    analytics["error"] = "no oauth secrets"
json.dump(analytics, open("analytics.json", "w", encoding="utf-8"), ensure_ascii=False)

rows = sorted(videos.values(), key=lambda v: v["published"])
prev = load("latest.json", {})
latest = {"updated": now, "subscribers": subs if subs is not None else prev.get("subscribers"), "videos": rows}
json.dump(latest, open("latest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

hist = load("history.json", [])
for v in rows:
    hist.append({"ts": now, "platform": "YouTube", "id": v["id"], "title": v["title"], "views": v["views"], "likes": v["likes"], "comments": v["comments"]})
json.dump(hist[-5000:], open("history.json", "w", encoding="utf-8"), ensure_ascii=False)
print("ok", len(rows), "videos")
