import asyncio
import os
from datetime import datetime

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

# =========================================
# НАСТРОЙКИ
# =========================================

# ВСТАВЬ СЮДА ID ВАШЕЙ ГРУППЫ
GROUP_ID = -1003462381248

TEAM = [
    "Егор",
    "Лена",
    "Аня",
    "Марсель",
    "Никита",
    "Тарас",
    "Юля",
    "Марічка",
]

# Языки пользователей
user_languages = {}
# Последние сообщения бота
last_bot_messages = {}

# =========================================
# ТЕКСТЫ
# =========================================

texts = {

    "ru": {
        "welcome": "🔥 Street Friends Bot\nДобро пожаловать!",

        "money": "💰 Общак",
        "cleaning": "🧹 Закрытие точки",
        "opening": "☀️ Открытие точки",
        "rent": "🏠 Аренда",
        "team": "👥 Команда",
        "fests": "🎉 Фесты",
        "schedule": "📅 Смены",
        "points": "📍 Точки",
        "settings": "⚙️ Настройки",
        "back": "⬅️ Назад",
    },

    "ua": {
        "welcome": "🔥 Street Friends Bot\nЛаскаво просимо!",

        "money": "💰 Общак",
        "cleaning": "🧹 Закриття точки",
        "opening": "☀️ Відкриття точки",
        "rent": "🏠 Оренда",
        "team": "👥 Команда",
        "fests": "🎉 Фести",
        "schedule": "📅 Зміни",
        "points": "📍 Точки",
        "settings": "⚙️ Налаштування",
        "back": "⬅️ Назад",
    },

    "it": {
        "welcome": "🔥 Street Friends Bot\nBenvenuto!",

        "money": "💰 Fondo comune",
        "cleaning": "🧹 Chiusura punto",
        "opening": "☀️ Apertura punto",
        "rent": "🏠 Affitto",
        "team": "👥 Squadra",
        "fests": "🎉 Festival",
        "schedule": "📅 Turni",
        "points": "📍 Punti",
        "settings": "⚙️ Impostazioni",
        "back": "⬅️ Indietro",
    },
}

# =========================================
# КНОПКИ ВЫБОРА ЯЗЫКА
# =========================================

language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🇷🇺 Русский",
                callback_data="lang_ru"
            ),
            InlineKeyboardButton(
                text="🇺🇦 Українська",
                callback_data="lang_ua"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🇮🇹 Italiano",
                callback_data="lang_it"
            ),
        ],
    ]
)

# =========================================
# ГЛАВНОЕ МЕНЮ
# =========================================

def get_menu(lang):

    return ReplyKeyboardMarkup(
        keyboard=[

            [
                KeyboardButton(text=texts[lang]["opening"]),
                KeyboardButton(text=texts[lang]["cleaning"]),
            ],

            [
                KeyboardButton(text=texts[lang]["money"]),
                KeyboardButton(text=texts[lang]["rent"]),
            ],

            [
                KeyboardButton(text=texts[lang]["schedule"]),
                KeyboardButton(text=texts[lang]["points"]),
            ],

            [
                KeyboardButton(text=texts[lang]["team"]),
                KeyboardButton(text=texts[lang]["fests"]),
            ],

            [
                KeyboardButton(text=texts[lang]["settings"]),
            ],
        ],
        resize_keyboard=True,
    )

# =========================================
# КНОПКА НАЗАД
# =========================================

def back_keyboard(lang):

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=texts[lang]["back"]
                )
            ]
        ],
        resize_keyboard=True,
    )
# =========================================
# УДАЛЕНИЕ ПРЕДЫДУЩИХ СООБЩЕНИЙ БОТА
# =========================================

async def send_clean_message(
    message: types.Message,
    text,
    reply_markup=None
):

    chat_id = message.chat.id

    # Удаляем старое сообщение бота
    if chat_id in last_bot_messages:

        try:

            await bot.delete_message(
                chat_id,
                last_bot_messages[chat_id]
            )

        except:
            pass

    # Отправляем новое сообщение
    sent_message = await message.answer(
        text,
        reply_markup=reply_markup
    )

    # Сохраняем ID сообщения
    last_bot_messages[chat_id] = sent_message.message_id
# =========================================
# /START
# =========================================

@dp.message(Command("start"))
async def start(message: types.Message):

    await message.answer(
        "🌍 Choose language / Оберіть мову / Scegli lingua",
        reply_markup=language_keyboard,
    )
# =========================================
# /RESTART
# =========================================

@dp.message(Command("restart"))
async def restart(message: types.Message):

    chat_id = message.chat.id

    # Удаляем последнее сообщение бота
    if chat_id in last_bot_messages:

        try:

            await bot.delete_message(
                chat_id,
                last_bot_messages[chat_id]
            )

        except:
            pass

    # Показываем выбор языка заново
    sent_message = await message.answer(
        "🔄 Бот перезапущен\n\n🌍 Choose language / Оберіть мову / Scegli lingua",
        reply_markup=language_keyboard,
    )

    # Сохраняем новое сообщение
    last_bot_messages[chat_id] = sent_message.message_id
# =========================================
# ВЫБОР ЯЗЫКА
# =========================================

@dp.callback_query()
async def language_selected(callback: types.CallbackQuery):

    lang = callback.data.split("_")[1]

    user_languages[callback.from_user.id] = lang

    await callback.message.answer(
        texts[lang]["welcome"],
        reply_markup=get_menu(lang),
    )

    await callback.answer()

# =========================================
# МЕНЮ
# =========================================

@dp.message()
async def menu_buttons(message: types.Message):

    lang = user_languages.get(
        message.from_user.id,
        "ru"
    )

    # =====================================
    # НАЗАД
    # =====================================

    if message.text == texts[lang]["back"]:

        await message.answer(
            "🏠 Главное меню",
            reply_markup=get_menu(lang)
        )

    # =====================================
    # ОТКРЫТИЕ ТОЧКИ
    # =====================================

    elif message.text == texts[lang]["opening"]:

        await message.answer(
            "☀️ ОТКРЫТИЕ ТОЧКИ\n\n"

            "1. Проверить заряд павербанков 🔋\n\n"

            "2. Надежно подключить зарядный кабель 🔌\n\n"

            "3. Проверить наличие:\n"
            "• краски\n"
            "• резинок\n"
            "• прищепок\n"
            "• влажных салфеток\n"
            "• дождевика\n"
            "• зонта\n\n"

            "4. Осмотреть ТОЧКУ на дефекты 👀\n\n"

            "🔥 И В БОЙ!",

            reply_markup=back_keyboard(lang)
        )

    # =====================================
    # ЗАКРЫТИЕ ТОЧКИ
    # =====================================

    elif message.text == texts[lang]["cleaning"]:

        await message.answer(
            "🌙 ЗАКРЫТИЕ СМЕНЫ\n\n"

            "1. Выключить программы 📸\n\n"

            "2. Выключить ноутбук и фотоаппарат 💻\n\n"

            "3. Залить краску в принтер 🖨️\n\n"

            "4. Поставить точку на зарядку 🔋\n\n"

            "5. Убрать мусор 🧹\n\n"

            "6. Протереть точку ✨\n\n"

            "7. Выкинуть мусор из офиса 🗑️",

            reply_markup=back_keyboard(lang)
        )

    # =====================================
    # ОБЩАК
    # =====================================

    elif message.text == texts[lang]["money"]:

        await message.answer(
            "💰 ОБЩАК\n\n"

            "Каждое воскресенье:\n"
            "25€ с человека ❤️",

            reply_markup=back_keyboard(lang)
        )

    # =====================================
    # АРЕНДА
    # =====================================

    elif message.text == texts[lang]["rent"]:

        await message.answer(
            "🏠 АРЕНДА ОФИСА\n\n"

            "Следующая оплата:\n"
            "01.06\n\n"

            "Далее каждые 2 месяца.",

            reply_markup=back_keyboard(lang)
        )

    # =====================================
    # СМЕНЫ
    # =====================================

    elif message.text == texts[lang]["schedule"]:

        await message.answer(
            "📅 СМЕНЫ\n\n"

            "ТОЧКА 1 🟢\n"
            "10:00 - 13:00\n"
            "13:00 - 15:30\n"
            "15:30 - 18:00\n"
            "18:00 - 21:00\n\n"

            "ТОЧКА 2 🔴\n"
            "10:00 - 13:00\n"
            "13:00 - 15:30\n"
            "15:30 - 18:00\n"
            "18:00 - 21:00",

            reply_markup=back_keyboard(lang)
        )

    # =====================================
    # ТОЧКИ
    # =====================================

    elif message.text == texts[lang]["points"]:

        await message.answer(
            "📍 STREET FRIENDS\n\n"

            "🟢 ТОЧКА 1 — Зеленая\n"
            "🔴 ТОЧКА 2 — Красная\n\n"

            "📸 Автономные фототочки.\n"
            "Работаем на ТОЛЕДО ❤️",

            reply_markup=back_keyboard(lang)
        )

    # =====================================
    # КОМАНДА
    # =====================================

    elif message.text == texts[lang]["team"]:

        team_text = "\n".join(
            [f"• {name}" for name in TEAM]
        )

        await message.answer(
            f"👥 STREET FRIENDS TEAM\n\n{team_text}",
            reply_markup=back_keyboard(lang)
        )

    # =====================================
    # ФЕСТЫ
    # =====================================

    elif message.text == texts[lang]["fests"]:

        await message.answer(
            "🎉 ФЕСТЫ\n\n"
            "Раздел пока в разработке 🔥",

            reply_markup=back_keyboard(lang)
        )

    # =====================================
    # НАСТРОЙКИ
    # =====================================

    elif message.text == texts[lang]["settings"]:

        await message.answer(
            "⚙️ НАСТРОЙКИ\n\n"
            "Чтобы сменить язык — нажмите /start",

            reply_markup=back_keyboard(lang)
        )

# =========================================
# АВТОНАПОМИНАНИЯ
# =========================================

async def auto_reminders():

    while True:

        now = datetime.now()

        # =====================================
        # УТРЕННЕЕ НАПОМИНАНИЕ
        # =====================================

        if now.hour == 9 and now.minute == 0:

            await bot.send_message(
                GROUP_ID,

                "☀️ STREET FRIENDS\n\n"

                "Напоминание об открытии ТОЧКИ:\n\n"

                "• проверить павербанки 🔋\n"
                "• проверить шнур питания 🔌\n"
                "• проверить расходники 📦\n"
                "• осмотреть ТОЧКУ 👀\n\n"

                "🔥 Хорошей работы на ТОЛЕДО!"
            )

        # =====================================
        # ВЕЧЕРНЕЕ НАПОМИНАНИЕ
        # =====================================

        if now.hour == 20 and now.minute == 45:

            await bot.send_message(
                GROUP_ID,

                "🌙 STREET FRIENDS\n\n"

                "Напоминание о закрытии ТОЧКИ:\n\n"

                "• выключить программы 📸\n"
                "• выключить ноутбук 💻\n"
                "• зарядить ТОЧКУ 🔋\n"
                "• зарядить павербанки 🔌\n"
                "• убрать мусор 🧹"
            )

        # =====================================
                # =====================================
        # ДЕЖУРСТВО В ОФИСЕ
        # =====================================

        if (
            now.weekday() == 3 and
            now.hour == 12 and
            now.minute == 0
        ):

            duty_text = "\n".join(
                [f"• {name}" for name in office_duty]
            )

            await bot.send_message(
                GROUP_ID,

                "🧹 STREET FRIENDS\n\n"

                "Напоминание про уборку офиса:\n\n"

                f"{duty_text}\n\n"

                "Что нужно сделать:\n"
                "• подмести офис\n"
                "• вынести мусор\n"
                "• протереть поверхности\n"
                "• проверить зарядки\n"
                "• навести порядок ❤️"
            )
        # ОБЩАК
        # =====================================

        if (
            now.weekday() == 6 and
            now.hour == 12 and
            now.minute == 0
        ):

            await bot.send_message(
                GROUP_ID,

                "💰 STREET FRIENDS\n\n"

                "Напоминание:\n"
                "Сегодня каждый участник кладет 25€ в ОБЩАК ❤️"
            )

        # =====================================
        # АРЕНДА
        # =====================================

        if (
            now.day == 1 and
            now.month in [2, 4, 6, 8, 10, 12] and
            now.hour == 12 and
            now.minute == 0
        ):

            await bot.send_message(
                GROUP_ID,

                "🏠 STREET FRIENDS\n\n"

                "Напоминание:\n"
                "Сегодня оплата аренды офиса 💸"
            )

        await asyncio.sleep(60)

# =========================================
# MAIN
# =========================================

async def main():

    print("BOT STARTED")

    asyncio.create_task(
        auto_reminders()
    )

    await dp.start_polling(bot)

# =========================================

if __name__ == "__main__":
    asyncio.run(main())