import requests
import re

# Самые стабильные базы с платными каналами
SOURCES = [
    "https://raw.githubusercontent.com/Fomitchev/IPTV/main/main.m3u",
    "https://smarttvnews.ru/apps/iptvchannels.m3u",
    "https://iptv.online/playlist/free.m3u",
    "https://raw.githubusercontent.com/vasiliy78L/IPTV/master/viju.m3u",
    "https://webarmen.com/my/iptv/auto.m3u"
]

def main():
    print("Запуск агрегатора...")
    # Заголовок с программой передач и логотипами
    playlist = "#EXTM3U x-tvg-url=\"http://www.webstrees.com/epg.xml.gz\"\n"
    seen = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=30, headers=headers)
            if r.status_code == 200:
                # Поиск пар: строка с названием + строка с ссылкой
                matches = re.findall(r"(#EXTINF:.*?\nhttp.*)", r.text, re.MULTILINE)
                for item in matches:
                    url_only = item.split('\n')[-1].strip()
                    if url_only not in seen:
                        playlist += item + "\n"
                        seen.add(url_only)
        except:
            continue
            
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print(f"Успех! Собрано каналов: {len(seen)}")

if __name__ == "__main__":
    main()
