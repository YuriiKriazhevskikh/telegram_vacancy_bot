import asyncio
from telethon import TelegramClient, events
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply('Привет! Я бот-эхо!!! Отправь мне любое сообщение, и я отвечу тем же.')

@bot.on(events.NewMessage)
async def echo(event):
    if event.out:
        return
    text = event.raw_text
    await event.reply(text)

async def main():
    await bot.start()
    print('Бот запущен и работает...')
    await bot.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()