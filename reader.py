import asyncio
import requests
from telethon import TelegramClient
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE_NUMBER')
BOT_TOKEN = os.getenv('BOT_TOKEN')
YOUR_USER_ID = 641810461

client = TelegramClient('user_session', API_ID, API_HASH)

KEYWORDS = ['python', 'стажёр', 'стажер', 'qa', 'тестировщик', 'junior']
EXCLUDE = ['senior', 'lead', 'тимлид', 'manager']
CHECK_INTERVAL = 1 * 60  # 30 минут
SENT_FILE = 'sent_messages.txt'  # файл для хранения ID отправленных сообщений

def load_sent_ids():
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, 'r') as f:
        return set(int(line.strip()) for line in f if line.strip().isdigit())

def save_sent_id(msg_id):
    with open(SENT_FILE, 'a') as f:
        f.write(f"{msg_id}\n")

def send_via_bot(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': YOUR_USER_ID, 'text': text, 'parse_mode': 'HTML'}
    try:
        r = requests.post(url, data=payload, timeout=10)
        if r.status_code == 200:
            print('✓ Отправлено через бота')
        else:
            print(f'✗ Ошибка отправки: {r.text}')
    except Exception as e:
        print(f'✗ Исключение при отправке: {e}')

async def check_channel():
    channel_username = 'qa_jobs'  # замените на ваш канал
    channel = await client.get_entity(channel_username)
    sent_ids = load_sent_ids()
    new_found = False

    async for msg in client.iter_messages(channel, limit=50):  # проверяем последние 50
        if msg.id in sent_ids:
            continue  # уже отправлено
        if msg.text:
            text_lower = msg.text.lower()
            if any(kw in text_lower for kw in KEYWORDS) and not any(ex in text_lower for ex in EXCLUDE):
                print(f'🔔 Новое подходящее сообщение (id={msg.id}), отправляем...')
                send_via_bot(msg.text)
                save_sent_id(msg.id)
                new_found = True
    if not new_found:
        print('Новых подходящих сообщений не найдено.')

async def main():
    await client.start(phone=PHONE)
    print('✅ Авторизация успешна. Запущен цикл проверки каждые 30 минут.')
    while True:
        print(f'\n--- Проверка канала в {time.strftime("%Y-%m-%d %H:%M:%S")} ---')
        try:
            await check_channel()
        except Exception as e:
            print(f'Ошибка при проверке канала: {e}')
        print(f'Ожидание {CHECK_INTERVAL // 60} минут до следующей проверки...')
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    asyncio.run(main())