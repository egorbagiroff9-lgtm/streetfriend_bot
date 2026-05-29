import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Общак")],
        [KeyboardButton(text="🧹 Уборки")],
        [KeyboardButton(text="🏠 Аренда")],
        [KeyboardButton(text="🎉 Фесты")],
        [KeyboardButton(text="⚙️ Настройки")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Бот администратора запущен!",
        reply_markup=menu
    )

@dp.message()
async def buttons(message: types.Message):

    if message.text == "💰 Общак":
        await message.answer("Раздел общака")

    elif message.text == "🧹 Уборки":
        await message.answer("График уборок")

    elif message.text == "🏠 Аренда":
        await message.answer("Информация об аренде")

    elif message.text == "🎉 Фесты":
        await message.answer("Список мероприятий")

    elif message.text == "⚙️ Настройки":
        await message.answer("Настройки бота")

async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())