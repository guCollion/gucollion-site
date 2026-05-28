import requests
import yaml

INPUT_FILE = "data/videos_source.yaml"
OUTPUT_FILE = "data/videos.yaml"

def get_video_info(bvid):
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bilibili.com/"
    }

    r = requests.get(url, headers=headers, timeout=10)
    data = r.json()

    if data.get("code") != 0:
        raise Exception(data.get("message", "获取失败"))

    info = data["data"]

    return {
        "title": info["title"],
        "desc": info["desc"][:80],
        "cover": info["pic"],
        "tag": info["owner"]["name"],
        "views": str(info["stat"]["view"]),
        "time": "Bilibili",
        "bvid": bvid,
    }

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    source = yaml.safe_load(f)

videos = []

for item in source:
    bvid = item["bvid"]
    print(f"正在获取：{bvid}")
    videos.append(get_video_info(bvid))

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    yaml.dump(videos, f, allow_unicode=True, sort_keys=False)

print("完成：data/videos.yaml 已更新")