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
rss_err = None
for _try in range(3):
    try:
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
        break
    except Exception as ex:
        rss_err = repr(ex)[:200]
        import time
        time.sleep(3)
if not videos:
    print("rss failed:", rss_err)

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

        if not videos:
            up = api("https://www.googleapis.com/youtube/v3/channels?" + urllib.parse.urlencode({"part": "contentDetails", "mine": "true"}))["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            for it in api("https://www.googleapis.com/youtube/v3/playlistItems?" + urllib.parse.urlencode({"part": "snippet,contentDetails", "playlistId": up, "maxResults": "50"}))["items"]:
                vid = it["contentDetails"]["videoId"]
                videos[vid] = {"id": vid, "title": it["snippet"]["title"], "published": it["contentDetails"].get("videoPublishedAt") or it["snippet"]["publishedAt"], "views": 0, "likes": 0, "comments": None}
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

        def safe(key, fn):
            try:
                analytics[key] = fn()
            except Exception as ex:
                analytics[key] = []
                analytics.setdefault("partial", {})[key] = repr(ex)[:200]

        safe("daily", lambda: rep("views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost,likes,comments,shares", "day", {"sort": "day"}))
        safe("videos", lambda: rep("views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments,shares", "video", {"sort": "-views", "maxResults": "50"}))
        safe("traffic", lambda: rep("views", "insightTrafficSourceType", {"sort": "-views"}))
        safe("countries", lambda: rep("views", "country", {"sort": "-views", "maxResults": "10"}))
        safe("demo", lambda: rep("viewerPercentage", "ageGroup,gender", {"sort": "-viewerPercentage"}))
        safe("devices", lambda: rep("views", "deviceType", {"sort": "-views"}))
        safe("subscribed", lambda: rep("views,estimatedMinutesWatched", "subscribedStatus", {"sort": "-views"}))

        def retention():
            out = {}
            for vid in videos:
                q = {"ids": "channel==MINE", "startDate": start, "endDate": end, "metrics": "audienceWatchRatio,relativeRetentionPerformance", "dimensions": "elapsedVideoTimeRatio", "filters": "video==" + vid}
                r = api("https://youtubeanalytics.googleapis.com/v2/reports?" + urllib.parse.urlencode(q))
                out[vid] = [[row[0], row[1], row[2]] for row in r.get("rows", [])]
            return out
        safe("retention", retention)

        def recent_comments():
            r = api("https://www.googleapis.com/youtube/v3/commentThreads?" + urllib.parse.urlencode({"part": "snippet", "allThreadsRelatedToChannelId": CH, "maxResults": "30", "order": "time"}))
            out = []
            for it in r.get("items", []):
                sn = it["snippet"]["topLevelComment"]["snippet"]
                out.append({"video": it["snippet"].get("videoId"), "author": sn.get("authorDisplayName"), "text": sn.get("textDisplay", "")[:300], "likes": sn.get("likeCount", 0), "at": sn.get("publishedAt")})
            return out
        safe("recent_comments", recent_comments)
        analytics["totals"] = {"start": start, "end": end}
    except Exception as e:
        analytics["error"] = repr(e)[:300]
else:
    analytics["error"] = "no oauth secrets"
json.dump(analytics, open("analytics.json", "w", encoding="utf-8"), ensure_ascii=False)

if not videos:
    print("no videos fetched; keeping previous data")
    raise SystemExit(0)
rows = sorted(videos.values(), key=lambda v: v["published"])
prev = load("latest.json", {})
latest = {"updated": now, "subscribers": subs if subs is not None else prev.get("subscribers"), "videos": rows}
json.dump(latest, open("latest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

hist = load("history.json", [])
for v in rows:
    hist.append({"ts": now, "platform": "YouTube", "id": v["id"], "title": v["title"], "views": v["views"], "likes": v["likes"], "comments": v["comments"]})
json.dump(hist[-5000:], open("history.json", "w", encoding="utf-8"), ensure_ascii=False)
print("ok", len(rows), "videos")
