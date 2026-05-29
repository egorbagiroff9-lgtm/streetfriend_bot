import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранение языков пользователей
user_languages = {}

# Тексты
texts = {
    "ru": {
        "welcome": "👋 Добро пожаловать в Street Friends!\nВыберите раздел:",
        "choose_language": "🌍 Выберите язык:",

        "schedule": "📅 Мои смены",
        "point1": "🟢 ТОЧКА 1",
        "point2": "🔴 ТОЧКА 2",
        "money": "💰 Общак",
        "office": "🏢 Офис",
        "open": "☀️ Открытие",
        "close": "🔒 Закрытие",
        "team": "👥 Команда",
    },

    "ua": {
        "welcome": "👋 Ласкаво просимо до Street Friends!\nОберіть розділ:",
        "choose_language": "🌍 Оберіть мову:",

        "schedule": "📅 Мої зміни",
        "point1": "🟢 ТОЧКА 1",
        "point2": "🔴 ТОЧКА 2",
        "money": "💰 Общак",
        "office": "🏢 Офіс",
        "open": "☀️ Відкриття",
        "close": "🔒 Закриття",
        "team": "👥 Команда",
    },

    "it": {
        "welcome": "👋 Benvenuto in Street Friends!\nScegli una sezione:",
        "choose_language": "🌍 Scegli la lingua:",

        "schedule": "📅 I miei turni",
        "point1": "🟢 PUNTO 1",
        "point2": "🔴 PUNTO 2",
        "money": "💰 Fondo comune",
        "office": "🏢 Ufficio",
        "open": "☀️ Apertura",
        "close": "🔒 Chiusura",
        "team": "👥 Squadra",
    },
}

# Кнопки выбора языка
language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_ua"),
        ],
        [
            InlineKeyboardButton(text="🇮🇹 Italiano", callback_data="lang_it"),
        ],
    ]
)

# Главное меню
def get_menu(lang):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts[lang]["schedule"])],
            [KeyboardButton(text=texts[lang]["point1"])],
            [KeyboardButton(text=texts[lang]["point2"])],
            [KeyboardButton(text=texts[lang]["money"])],
            [KeyboardButton(text=texts[lang]["office"])],
            [KeyboardButton(text=texts[lang]["open"])],
            [KeyboardButton(text=texts[lang]["close"])],
            [KeyboardButton(text=texts[lang]["team"])],
        ],
        resize_keyboard=True,
    )


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🌍 Choose language / Оберіть мову / Scegli lingua",
        reply_markup=language_keyboard,
    )


@dp.callback_query()
async def language_selected(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]

    user_languages[callback.from_user.id] = lang

    await callback.message.answer(
        texts[lang]["welcome"],
        reply_markup=get_menu(lang),
    )

    await callback.answer()


@dp.message()
async def menu_buttons(message: types.Message):

    lang = user_languages.get(message.from_user.id, "ru")

    if message.text == texts[lang]["schedule"]:
        await message.answer(
            "📅 Смены:\n\n"
            "1️⃣ 10:00–13:00\n"
            "2️⃣ 13:00–15:30\n"
            "3️⃣ 15:30–18:00\n"
            "4️⃣ 18:00–21:00"
        )

    elif message.text == texts[lang]["point1"]:
        await message.answer("🟢 ТОЧКА 1 — Зеленая точка активна")

    elif message.text == texts[lang]["point2"]:
        await message.answer("🔴 ТОЧКА 2 — Красная точка активна")

    elif message.text == texts[lang]["money"]:
        await message.answer(
            "💰 ОБЩАК\n\n"
            "Каждое воскресенье:\n"
            "25€ с человека"
        )

    elif message.text == texts[lang]["office"]:
        await message.answer(
            "🏢 ОФИС\n\n"
            "Следующая аренда:\n"
            "01.06"
        )

    elif message.text == texts[lang]["open"]:
        await message.answer(
            "☀️ ОТКРЫТИЕ ТОЧКИ\n\n"
            "1. Проверить заряд павербанков\n"
            "2. Проверить шнур питания\n"
            "3. Проверить краску\n"
            "4. Проверить салфетки\n"
            "5. Проверить зонтик/дождевик\n"
            "6. Осмотреть точку"
        )

    elif message.text == texts[lang]["close"]:
        await message.answer(
            "🔒 ЗАКРЫТИЕ ТОЧКИ\n\n"
            "1. Выключить программы\n"
            "2. Выключить ноутбук\n"
            "3. Выключить фотоаппарат\n"
            "4. Залить краску\n"
            "5. Поставить всё на зарядку\n"
            "6. Убрать мусор\n"
            "7. Протереть точку"
        )

    elif message.text == texts[lang]["team"]:
        await message.answer(
            "👥 КОМАНДА STREET FRIENDS\n\n"
            "• Егор\n"
            "• Лена\n"
            "• Аня\n"
            "• Марсель\n"
            "• Никита\n"
            "• Тарас\n"
            "• Юля\n"
            "• Марічка"
        )


async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())