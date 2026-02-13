import requests
import re

# Новые, расширенные источники (включая CineMan, MiniMax и Viju)
SOURCES = [
    "https://raw.githubusercontent.com/Fomitchev/IPTV/main/main.m3u",
    "https://smarttvnews.ru/apps/iptvchannels.m3u",
    "http://siptv.app/lists/ru.m3u", # Резервный источник для Viju
    "https://iptv.online/playlist/free.m3u", # Основной источник для 4K и CineMan
    "https://raw.githubusercontent.com/vasiliy78L/IPTV/master/viju.m3u" # Прямая база Viju
]

def main():
    print("Запуск захвата VIP-каналов...")
    playlist = "#EXTM3U x-tvg-url=\"http://www.webstrees.com/epg.xml.gz\"\n"
    seen = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=20, headers=headers)
            if r.status_code == 200:
                # Улучшенный поиск, захватывающий категории и логотипы
                items = re.findall(r"(#EXTINF:.*?\nhttp.*)", r.text, re.MULTILINE)
                for item in items:
                    # Очистка ссылки от мусора
                    link = item.split('\n')[-1].strip()
                    if link not in seen:
                        # Проверка, есть ли в названии нужные нам ключевые слова
                        name = item.lower()
                        # Если хочешь только свой список, можно добавить фильтрацию тут
                        playlist += item + "\n"
                        seen.add(link)
            print(f"Источник {url} обработан.")
        except:
            print(f"Ошибка на источнике {url}")
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print(f"Сборка завершена! Всего каналов: {len(seen)}")

if __name__ == "__main__":
    main()
