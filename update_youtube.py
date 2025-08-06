import requests
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")
REGION = "KR"
MAX_RESULTS = 5

def get_trending_videos():
    url = (
        f"https://www.googleapis.com/youtube/v3/videos"
        f"?part=snippet,statistics&chart=mostPopular"
        f"&regionCode={REGION}&maxResults={MAX_RESULTS}&key={API_KEY}"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        return ["유튜브 인기영상을 불러오지 못했습니다."]
    videos = resp.json().get("items", [])
    result = []
    for v in videos:
        title = v["snippet"]["title"]
        channel = v["snippet"]["channelTitle"]
        link = f"https://youtube.com/watch?v={v['id']}"
        view = v["statistics"]["viewCount"]
        # 썸네일 이미지 (마크다운 이미지 링크)
        thumbnail = v["snippet"]["thumbnails"]["default"]["url"]
        result.append(f"![thumbnail]({thumbnail})\n[{title}]({link}) - {channel} ({int(view):,}회)")
    return result

def update_readme(videos):
    from datetime import datetime
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# 🇰🇷 오늘의 유튜브 실시간 인기 영상 Top 5\n\n")
        f.write("하루에 영상 5개만 보기.. 약속 \^o^/\n")
        f.write("시간은 금이다$¥฿₩€🪙\n")
        f.write("![gold](https://media.tenor.com/your-gif-id.gif)\n\n")
        f.write("\n")
        for i, video in enumerate(videos, 1):
            f.write(f"**{i}.** {video}\n\n")
        f.write(f"\n---\n")
        f.write(f"⏳ 마지막 업데이트: {now}\n")
        f.write("\nPowered by [YouTube Data API](https://developers.google.com/youtube/v3/docs/videos/list) · 자동화 봇")

if __name__ == "__main__":
    videos = get_trending_videos()
    update_readme(videos)
