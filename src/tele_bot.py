import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_message(message: types.Message):
    await message.answer("Hello!")


# Отправка уведомлений
async def send_notification(user_id: int, message_content: str):
    await bot.send_message(user_id, f'New message: {message_content}')


if __name__ == "__main__":
    asyncio.run(send_notification())

