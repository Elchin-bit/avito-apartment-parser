import requests
from bs4 import BeautifulSoup
import time
import json
import re
import asyncio
from telegram import Bot
from telegram.error import TelegramError



MIN_PRICE = 35000
MAX_PRICE = 45000

# Telegram
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"

CHECK_INTERVAL = 300  # 5 минут

# ========== ФУНКЦИИ ==========

def get_avito_url():
    """URL для ТОЛЬКО 2-комнатных"""
    return "https://www.avito.ru/kazan/kvartiry/sdam/na_dlitelnyy_srok/2-komnatnye-ASgBAgICA0SSA8gQ8AeQUswIkFk?pmin=35000&pmax=45000"


def is_two_room(title):
    """Проверяет 2-комнатную квартиру"""
    title_lower = title.lower()

    patterns = [
        r'2-к\.',
        r'2к\.',
        r'2-комн',
        r'2 комн',
        r'двухкомн',
        r'двушк'
    ]

    for pattern in patterns:
        if re.search(pattern, title_lower):
            return True

    if re.search(r'[13]-к\.', title_lower):
        return False
    if 'студия' in title_lower:
        return False

    return False


def get_page_content(url):
    """Получает HTML"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'ru-RU,ru;q=0.9',
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            return response.text
        elif response.status_code == 429:
            print("⚠️ Ошибка 429: Ждем 60 сек...")
            time.sleep(60)
            return None
        else:
            print(f"⚠️ Ошибка {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None


def parse_apartments(html_content):
    """Парсит ТОЛЬКО 2-комнатные"""
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    apartments = []

    json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})

    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)

            if '@graph' in data:
                for item in data['@graph']:
                    if item.get('@type') == 'Product' and 'offers' in item:
                        aggregate = item['offers']
                        if 'offers' in aggregate:
                            for offer in aggregate['offers']:
                                try:
                                    title = offer.get('name', '')
                                    price_str = offer.get('price', '0')
                                    price = int(price_str) if price_str else 0
                                    url = offer.get('url', '')

                                    if is_two_room(title):
                                        if MIN_PRICE <= price <= MAX_PRICE:
                                            apartments.append({
                                                'title': title,
                                                'price': price,
                                                'link': url
                                            })
                                            print(f"✅ {title} - {price:,} ₽")

                                except (KeyError, ValueError):
                                    continue

        except json.JSONDecodeError:
            continue

    print(f"📊 Найдено 2-комнатных: {len(apartments)}")
    return apartments


async def send_telegram_message(bot, apartments):
    """Отправка в Telegram (async)"""
    if not apartments or not bot:
        return

    for apt in apartments:
        message = f"""
🏠 <b>Новая 2-комнатная!</b>

💰 {apt['price']:,} ₽/мес
📝 {apt['title']}

🔗 <a href="{apt['link']}">Смотреть объявление</a>
        """

        try:
            await bot.send_message(
                chat_id=CHAT_ID,
                text=message.strip(),
                parse_mode='HTML',
                disable_web_page_preview=True
            )
            print(f"✅ Отправлено в Telegram")
            await asyncio.sleep(1)
        except TelegramError as e:
            print(f"❌ Telegram: {e}")


async def main():
    """Главная функция (async)"""
    print("=" * 60)
    print("🚀 Avito Parser — ТОЛЬКО 2-комнатные квартиры")
    print(f"💰 Цена: {MIN_PRICE:,} - {MAX_PRICE:,} ₽")
    print(f"⏰ Проверка каждые {CHECK_INTERVAL} сек")
    print("=" * 60)
    print()

    # Telegram
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        await bot.get_me()
        print("✅ Telegram подключен\n")
    except:
        print("⚠️ Telegram не работает\n")
        bot = None

    seen_links = set()

    try:
        while True:
            print(f"🔄 Проверка {time.strftime('%H:%M:%S')}")

            html = get_page_content(get_avito_url())

            if html:
                apartments = parse_apartments(html)

                new_apartments = [
                    apt for apt in apartments
                    if apt['link'] not in seen_links
                ]

                if new_apartments:
                    print(f"🆕 Новых: {len(new_apartments)}")

                    for apt in new_apartments:
                        seen_links.add(apt['link'])

                    if bot:
                        await send_telegram_message(bot, new_apartments)
                else:
                    print(f"📋 Всего: {len(apartments)}, новых: 0")

            print(f"⏳ Следующая проверка через {CHECK_INTERVAL} сек")
            print("=" * 60)
            print()
            await asyncio.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n⛔ Остановка")


if __name__ == "__main__":
    asyncio.run(main())
