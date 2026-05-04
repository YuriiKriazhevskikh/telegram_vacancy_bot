import asyncio
from telethon import TelegramClient, events
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Ключевые слова (можно менять)
KEYWORDS = ['python', 'стажёр', 'qa', 'тестирование']
EXCLUDE_WORDS = ['senior', 'lead', 'c++']

async def check_and_send(message_text, chat_username):
    """Проверяет сообщение на ключевые слова и отправляет, если подходит"""
    text_lower = message_text.lower()
    if any(kw in text_lower for kw in KEYWORDS) and not any(ew in text_lower for ew in EXCLUDE_WORDS):
        # Отправляем себе в личку (укажите свой username или ID)
        await bot.send_message('me', f'Найдена вакансия в {chat_username}:\n{message_text[:500]}')

async def main():
    await bot.start()
    print('Бот запущен для мониторинга открытых каналов')
    
    # Список каналов для мониторинга (username без @)
    channels = ['automatedqa']  # добавьте нужные
    
    for ch in channels:
        try:
            entity = await bot.get_entity(ch)
            print(f'Подключён к каналу {entity.title}')
        except Exception as e:
            print(f'Не удалось подключиться к {ch}: {e}')
    
    # Здесь нужно реализовать периодическую проверку новых сообщений.
    # Простейший способ: раз в минуту проверять последние несколько сообщений.
    # Более продвинутый: использовать events (но для каналов нужно быть администратором).
    
    while True:
        for ch in channels:
            try:
                entity = await bot.get_entity(ch)
                # Читаем последние 5 сообщений (можно увеличить)
                async for msg in bot.iter_messages(entity, limit=5):
                    if msg.text and not msg.out:
                        await check_and_send(msg.text, ch)
            except Exception as e:
                print(f'Ошибка при чтении {ch}: {e}')
        await asyncio.sleep(60)  # пауза 1 минута

if __name__ == '__main__':
    asyncio.run(main())