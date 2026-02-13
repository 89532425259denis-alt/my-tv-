import requests
import re

# Обновленный список "живых" доноров (Платные, CineMan, 4K)
SOURCES = [
    "https://iptv.ax/free.m3u",
    "https://smarttvnews.ru/apps/iptvchannels.m3u",
    "https://raw.githubusercontent.com/Fomitchev/IPTV/main/main.m3u",
    "https://webarmen.com/my/iptv/auto.m3u",
    "http://listiptv.ru/iptv.m3u"
]

def main():
    print("--- ЗАПУСК ГЛУБОКОГО СКАНИРОВАНИЯ ---")
    playlist = "#EXTM3U x-tvg-url=\"http://www.webstrees.com/epg.xml.gz\"\n"
    seen = set()
    # Усиленные заголовки, чтобы серверы не блокировали бота
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    for url in SOURCES:
        try:
            print(f"Сканирую: {url}")
            r = requests.get(url, timeout=30, headers=headers)
            if r.status_code == 200 and len(r.text) > 100:
                # Находим блоки: #EXTINF + любая строка + ссылка http
                items = re.findall(r"(#EXTINF:.*?\nhttp.*)", r.text, re.MULTILINE)
                print(f"Найдено каналов в источнике: {len(items)}")
                for item in items:
                    link = item.split('\n')[-1].strip()
                    if link not in seen:
                        playlist += item + "\n"
                        seen.add(link)
            else:
                print(f"Источник пуст или заблокирован (Status: {r.status_code})")
        except Exception as e:
            print(f"Ошибка соединения: {e}")
            continue
            
    if len(seen) > 0:
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(playlist)
        print(f"УСПЕХ! Всего собрано: {len(seen)} каналов.")
    else:
        print("КРИТИЧЕСКАЯ ОШИБКА: Ни один источник не отдал каналы!")

if __name__ == "__main__":
    main()
