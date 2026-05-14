import asyncio
import aiohttp
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
EXCLUDE = []  # можно добавить слова для исключения
CHECK_INTERVAL = 60 * 60  # 60 минут
SENT_FILE = 'sent_messages.txt'

# Список каналов (без @)
CHANNELS = [
    'YotolabQA',
    'qa_jobs',
    'rabotadlaqa',
    'qajobsru',
    'easy_qa_jobs',
    'qa_jobs_rabota',
    'jobforqa',
    'testerrjob',
    'qajoboffer',
    'jobGeeks',
    'qa_work'
]

def load_sent_ids():
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, 'r') as f:
        return set(int(line.strip()) for line in f if line.strip().isdigit())

def save_sent_id(msg_id):
    with open(SENT_FILE, 'a') as f:
        f.write(f"{msg_id}\n")

async def send_via_bot(text, max_retries=3):
    """Асинхронная отправка через бота с повторными попытками"""
    if len(text) > 3500:
        text = text[:3500] + "\n\n[Сообщение обрезано из-за длины]"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': YOUR_USER_ID, 'text': text, 'parse_mode': 'HTML'}

    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=payload, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status == 200:
                        print('✓ Отправлено через бота')
                        return True
                    elif resp.status == 429:
                        data = await resp.json()
                        retry_after = data.get('parameters', {}).get('retry_after', 5)
                        print(f'⚠️ Лимит запросов. Повтор через {retry_after} сек...')
                        await asyncio.sleep(retry_after)
                        continue
                    else:
                        print(f'✗ Ошибка HTTP {resp.status}: {await resp.text()}')
                        return False
        except Exception as e:
            print(f'✗ Исключение при отправке: {e}')
            await asyncio.sleep(2 ** attempt)  # экспоненциальная задержка
    return False

async def check_one_channel(channel_username):
    """Проверяет один канал, отправляет новые подходящие сообщения"""
    try:
        channel = await client.get_entity(channel_username)
        print(f'\n--- Проверка канала {channel.title} (@{channel_username}) ---')
    except Exception as e:
        print(f'Не удалось получить доступ к каналу {channel_username}: {e}')
        return

    sent_ids = load_sent_ids()
    new_found = False

    try:
        async for msg in client.iter_messages(channel, limit=20):
            if msg.id in sent_ids:
                continue
            if msg.text:
                text_lower = msg.text.lower()
                if any(kw in text_lower for kw in KEYWORDS) and not any(ex in text_lower for ex in EXCLUDE):
                    print(f'🔔 Новое подходящее сообщение из {channel_username} (id={msg.id})')
                    if await send_via_bot(msg.text):
                        save_sent_id(msg.id)
                        new_found = True
                    else:
                        print(f'⚠️ Сообщение {msg.id} не отправлено, ID не сохранён')
                    await asyncio.sleep(1.5)  # задержка между отправками
    except Exception as e:
        print(f'Ошибка при чтении канала {channel_username}: {e}')
        # Пробуем переподключить клиента
        await client.disconnect()
        await client.connect()
        print('Клиент Telethon переподключен')

    if not new_found:
        print(f'В канале {channel_username} новых подходящих сообщений нет.')

async def main():
    # Подключаемся и авторизуемся
    await client.start(phone=PHONE)
    print('✅ Авторизация успешна. Запущен цикл проверки всех каналов.')

    while True:
        print(f'\n=== Общая проверка в {time.strftime("%Y-%m-%d %H:%M:%S")} ===')
        for ch in CHANNELS:
            await check_one_channel(ch)
        print(f'Ожидание {CHECK_INTERVAL // 60} минут до следующей проверки...')
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nСкрипт остановлен пользователем.")