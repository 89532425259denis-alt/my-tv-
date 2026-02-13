import requests
import re

# Самые мощные источники с платными каналами (Viju, CineMan, 4K, Sport)
SOURCES = [
    "https://raw.githubusercontent.com/Fomitchev/IPTV/main/main.m3u",       # Спорт и Кинопремьеры
    "https://smarttvnews.ru/apps/iptvchannels.m3u",                       # Платные РФ (Viju, Амедиа)
    "https://iptv.online/playlist/free.m3u",                              # CineMan, MiniMax, 4K
    "https://raw.githubusercontent.com/vasiliy78L/IPTV/master/viju.m3u",   # Чистый пакет Viju/Viasat
    "https://webarmen.com/my/iptv/auto.m3u",                              # Самообновляемый премиум
    "https://y666.ru/iptv.m3u"                                            # Резерв премиум каналов
]

def main():
    print("Захват платных пакетов (Viju, CineMan, Match)...")
    playlist = "#EXTM3U x-tvg-url=\"http://www.webstrees.com/epg.xml.gz\"\n"
    seen_urls = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=25, headers=headers)
            if r.status_code == 200:
                # Ищем блоки данных (Название + Ссылка)
                items = re.findall(r"(#EXTINF:.*?\nhttp.*)", r.text, re.MULTILINE)
                for item in items:
                    link = item.split('\n')[-1].strip()
                    if link not in seen_urls:
                        # Убираем мусорные ссылки
                        if ".m3u8" in link or ".ts" in link or ".mpd" in link:
                            playlist += item + "\n"
                            seen_urls.add(link)
            print(f"Источник {url} — Успех.")
        except:
            print(f"Источник {url} — Пропущен.")
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print(f"Готово! Всего захвачено: {len(seen_urls)} каналов.")

if __name__ == "__main__":
    main()
