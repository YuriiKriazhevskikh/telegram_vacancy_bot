import asyncio
from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE_NUMBER')

client = TelegramClient('user_session', API_ID, API_HASH)

KEYWORDS = ['python', 'стажёр', 'стажер', 'qa', 'тестировщик', 'junior']  # что ищем
EXCLUDE = ['senior QA', 'lead', 'тимлид', 'manager']  # что исключаем

async def main():
    await client.connect()  # Подключаемся к серверу
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE)
        code = input('Введите код из Telegram: ')
        await client.sign_in(PHONE, code)
    print('✅ Авторизация успешна!')
    
    # Тестовый канал (можно заменить на ваш)
    channel_username = 'automatedqa'
    channel = await client.get_entity(channel_username)
    print(f'📢 Читаем последние 3 сообщения из канала {channel.title}')
    
    async for msg in client.iter_messages(channel, limit=3):
        if msg.text:
            print(f'---\n{msg.text}\n')

if __name__ == '__main__':
    asyncio.run(main())