import asyncio
from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

bot = TelegramClient('bot_for_channel', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def main():
    await bot.start()
    print('✅ Бот запущен')

    # Укажите username открытого канала (например, 'tbank' или 'durov')
    channel_username = 'automatedqa'
    channel = await bot.get_entity(channel_username)
    print(f'📢 Читаем последние 5 сообщений из канала {channel.title}\n')

    async for msg in bot.iter_messages(channel, limit=5):
        if msg.text:
            print(f'{msg.text}\n---\n')

    await bot.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()