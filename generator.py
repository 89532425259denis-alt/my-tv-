import requests
import re

SOURCES = [
    "https://raw.githubusercontent.com/Fomitchev/IPTV/main/main.m3u",
    "https://smarttvnews.ru/apps/iptvchannels.m3u",
    "https://iptv-org.github.io/iptv/countries/ru.m3u",
    "http://iptv.online/playlist/free.m3u"
]

def main():
    playlist = "#EXTM3U x-tvg-url=\"http://www.webstrees.com/epg.xml.gz\"\n"
    seen = set()
    headers = {'User-Agent': 'Mozilla/5.0'}
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15, headers=headers)
            if r.status_code == 200:
                items = re.findall(r"(#EXTINF:.*?\nhttp.*)", r.text, re.MULTILINE)
                for item in items:
                    link = item.split('\n')[-1].strip()
                    if link not in seen:
                        playlist += item + "\n"
                        seen.add(link)
        except: continue
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)

if __name__ == "__main__":
    main()
