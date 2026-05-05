import asyncio
from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE_NUMBER')
YOUR_USER_ID = 641810461

client = TelegramClient('user_session', API_ID, API_HASH)

async def main():
    await client.start(phone=PHONE)
    me = await client.get_me()
    print(f'Мой ID из скрипта: {me.id}')
    await client.send_message(YOUR_USER_ID, "Тестовое сообщение")
    print('Отправлено. Проверьте "Избранное" (Saved Messages)')
    await client.disconnect()

asyncio.run(main())