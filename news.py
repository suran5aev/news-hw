import sqlite3
from aiogram import Bot, Dispatcher, types, executor
from bs4 import BeautifulSoup
import requests
from config import token  

bot = Bot(token=token)
dp = Dispatcher(bot)

connection = sqlite3.connect('news.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS news(
    id INTEGER PRIMARY KEY,
    news VARCHAR (255)
);
""")

async def start(message: types.Message):
    await message.answer("Привет! Я бот новостей. Чтобы получить новости, введите команду /news.")

async def news(message: types.Message):
    for page in range(1, 11):
        url = f'https://24.kg/page_{page}'
        try:
            response = requests.get(url=url)    
            response.raise_for_status()  
            soup = BeautifulSoup(response.text, 'lxml')
            all_news = soup.find_all('div', class_='title')
        
            for news in all_news:
                news_text = news.text.strip()
                await message.answer(news_text)
                cursor.execute("INSERT INTO news (news) VALUES (?)", (news_text,))
                connection.commit()
        except Exception as e:
            await message.answer(f"Произошла ошибка при получении новостей: {e}")


@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    await start(message)

@dp.message_handler(commands=['news'])
async def handle_news(message: types.Message):
    await news(message)

executor.start_polling(dp)
