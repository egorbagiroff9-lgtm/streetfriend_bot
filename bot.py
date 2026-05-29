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

# Хранение языка пользователей
user_languages = {}

# Тексты
texts = {
    "ru": {
        "welcome": "👋 Добро пожаловать!\nВыберите раздел:",
        "choose_language": "🌍 Выберите язык:",
        "money": "💰 Общак",
        "cleaning": "🧹 Уборки",
        "rent": "🏠 Аренда",
        "fests": "🎉 Фесты",
        "settings": "⚙️ Настройки",
    },
    "ua": {
        "welcome": "👋 Ласкаво просимо!\nОберіть розділ:",
        "choose_language": "🌍 Оберіть мову:",
        "money": "💰 Общак",
        "cleaning": "🧹 Прибирання",
        "rent": "🏠 Оренда",
        "fests": "🎉 Фести",
        "settings": "⚙️ Налаштування",
    },
    "it": {
        "welcome": "👋 Benvenuto!\nScegli una sezione:",
        "choose_language": "🌍 Scegli la lingua:",
        "money": "💰 Fondo comune",
        "cleaning": "🧹 Pulizie",
        "rent": "🏠 Affitto",
        "fests": "🎉 Festival",
        "settings": "⚙️ Impostazioni",
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


def get_menu(lang):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts[lang]["money"])],
            [KeyboardButton(text=texts[lang]["cleaning"])],
            [KeyboardButton(text=texts[lang]["rent"])],
            [KeyboardButton(text=texts[lang]["fests"])],
            [KeyboardButton(text=texts[lang]["settings"])],
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

    if message.text == texts[lang]["money"]:
        await message.answer(texts[lang]["money"])

    elif message.text == texts[lang]["cleaning"]:
        await message.answer(texts[lang]["cleaning"])

    elif message.text == texts[lang]["rent"]:
        await message.answer(texts[lang]["rent"])

    elif message.text == texts[lang]["fests"]:
        await message.answer(texts[lang]["fests"])

    elif message.text == texts[lang]["settings"]:
        await message.answer(texts[lang]["settings"])


async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())