# 🏠 Avito Apartment Parser

Telegram bot for real-time monitoring of new apartment listings on Avito with customizable filters and instant notifications.

## 📋 Features

- **Real-time monitoring** - Checks Avito every 5 minutes for new listings
- **Smart filtering** - Only 2-bedroom apartments in Kazan (35,000-45,000 ₽/month)
- **Duplicate prevention** - Uses set-based tracking to avoid sending the same listing twice
- **Telegram integration** - Instant notifications with apartment details and direct links
- **Stable parsing** - Extracts data from JSON-LD (more reliable than HTML tags)

## 🛠️ Tech Stack

- **Python 3.10+**
- **Libraries:**
  - `requests` - HTTP requests to Avito
  - `beautifulsoup4` - HTML parsing and JSON-LD extraction
  - `python-telegram-bot` - Async Telegram API integration
  - `asyncio` - Asynchronous task handling

## 🚀 Quick Start

1. Clone the repository:
git clone https://github.com/Elchin-bit/avito-apartment-parser.git
cd avito-apartment-parser

2. Install dependencies:
pip install requests beautifulsoup4 python-telegram-bot

3. Configure your Telegram bot:
   - Create a bot via [@BotFather](https://t.me/BotFather)
   - Get your chat ID from [@userinfobot](https://t.me/userinfobot)
   - Update credentials in `parser.py`

4. Run the parser:
python parser.py

## 📊 How It Works

The parser follows this workflow:

1. **Fetches** HTML from Avito search page
2. **Extracts** JSON-LD structured data (SEO metadata)
3. **Filters** apartments by room count and price range
4. **Tracks** seen listings using set data structure
5. **Sends** new listings to Telegram with formatted messages

### Why JSON-LD?

Instead of parsing HTML tags (fragile), the bot extracts structured data that Avito provides for search engines. This approach is more stable when the website design changes.

## 🔧 Configuration

Edit parameters in `parser.py`:
MIN_PRICE = 35000 # Minimum price (₽/month)
MAX_PRICE = 45000 # Maximum price (₽/month)
CHECK_INTERVAL = 300 # Check frequency (seconds)

## 📱 Example Output

🏠 Новая 2-комнатная!

💰 45,000 ₽/мес
📝 2-к. квартира, 55 м², 8/9 эт.

🔗 Смотреть объявление

## ⚠️ Rate Limiting

The parser handles Avito's rate limiting (HTTP 429) automatically:
- Pauses for 60 seconds when blocked
- Resumes normal operation after cooldown

## 🎯 Future Improvements

- [ ] SQLite database for persistent storage
- [ ] Multiple location support
- [ ] Interactive Telegram keyboard buttons
- [ ] Price change notifications
- [ ] Apartment photos in messages

## 👨‍💻 Author

**Elchin Aliev**  
Junior IT Specialist | AI Enthusiast

Built with AI assistance (Claude Sonnet 4.5 via Perplexity)

## 📄 License

MIT License - Free to use for personal and educational purposes.

---

*Made for automating apartment hunting in Kazan* 🏙️
