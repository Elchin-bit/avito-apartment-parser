import asyncio
from telegram import Bot

TOKEN = "8192916703:AAF-LtZ4fVC7Pw8ODbBM5jL_g8vcGQCwKWU"
CHAT_ID = "210687006"

async def send_test():
    bot = Bot(token=TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text="🚀 ТЕСТ! Если видишь — всё работает!"
    )
    print("✅ Сообщение отправлено!")

if __name__ == "__main__":
    asyncio.run(send_test())
