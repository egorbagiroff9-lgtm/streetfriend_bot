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

# Языки пользователей
user_languages = {}

# Тексты
texts = {
    "ru": {
        "welcome": "🔥 Street Friends Bot\nДобро пожаловать!",
        "choose_language": "🌍 Выберите язык:",
        "money": "💰 Общак",
        "cleaning": "🧹 Закрытие смены",
        "opening": "🌅 Открытие точки",
        "rent": "🏠 Аренда офиса",
        "team": "👥 Команда",
        "settings": "⚙️ Настройки",
    },

    "ua": {
        "welcome": "🔥 Street Friends Bot\nЛаскаво просимо!",
        "choose_language": "🌍 Оберіть мову:",
        "money": "💰 Общак",
        "cleaning": "🧹 Закриття зміни",
        "opening": "🌅 Відкриття точки",
        "rent": "🏠 Оренда офісу",
        "team": "👥 Команда",
        "settings": "⚙️ Налаштування",
    },

    "it": {
        "welcome": "🔥 Street Friends Bot\nBenvenuto!",
        "choose_language": "🌍 Scegli la lingua:",
        "money": "💰 Fondo comune",
        "cleaning": "🧹 Chiusura turno",
        "opening": "🌅 Apertura punto",
        "rent": "🏠 Affitto ufficio",
        "team": "👥 Squadra",
        "settings": "⚙️ Impostazioni",
    },
}

# Кнопки выбора языка
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

# Главное меню
def get_menu(lang):

    return ReplyKeyboardMarkup(
        keyboard=[

            [
                KeyboardButton(
                    text=texts[lang]["money"]
                )
            ],

            [
                KeyboardButton(
                    text=texts[lang]["cleaning"]
                )
            ],

            [
                KeyboardButton(
                    text=texts[lang]["opening"]
                )
            ],

            [
                KeyboardButton(
                    text=texts[lang]["rent"]
                )
            ],

            [
                KeyboardButton(
                    text=texts[lang]["team"]
                )
            ],

            [
                KeyboardButton(
                    text=texts[lang]["settings"]
                )
            ],
        ],
        resize_keyboard=True,
    )


# START
# Получение ID чата
@dp.message(Command("id"))
async def get_chat_id(message: types.Message):

    await message.answer(
        f"🆔 Chat ID:\n{message.chat.id}"
    )
@dp.message(Command("start"))
async def start(message: types.Message):

    await message.answer(
        "🌍 Choose language / Оберіть мову / Scegli lingua",
        reply_markup=language_keyboard,
    )


# Выбор языка
@dp.callback_query()
async def language_selected(callback: types.CallbackQuery):

    lang = callback.data.split("_")[1]

    user_languages[callback.from_user.id] = lang

    await callback.message.answer(
        texts[lang]["welcome"],
        reply_markup=get_menu(lang),
    )

    await callback.answer()


# Кнопки меню
@dp.message()
async def menu_buttons(message: types.Message):

    lang = user_languages.get(
        message.from_user.id,
        "ru"
    )

    # ОБЩАК
    if message.text == texts[lang]["money"]:

        if lang == "ru":
            await message.answer(
                "💰 Напоминание:\n"
                "Каждое воскресенье каждый участник кладет 25€ в общак."
            )

        elif lang == "ua":
            await message.answer(
                "💰 Нагадування:\n"
                "Щонеділі кожен учасник кладе 25€ в общак."
            )

        elif lang == "it":
            await message.answer(
                "💰 Promemoria:\n"
                "Ogni domenica ogni membro mette 25€ nel fondo comune."
            )

    # ЗАКРЫТИЕ СМЕНЫ
    elif message.text == texts[lang]["cleaning"]:

        if lang == "ru":
            await message.answer(
                "🧹 Закрытие смены:\n\n"
                "1. Выключить программы фотоаппарата и печати\n"
                "2. Выключить ноутбук и фотоаппарат\n"
                "3. Залить краску в принтер и выключить его\n"
                "4. Поставить точку и павербанки на зарядку\n"
                "5. Убрать мусор и протереть точку\n"
                "6. Выкинуть мусор с офиса"
            )

        elif lang == "ua":
            await message.answer(
                "🧹 Закриття зміни:\n\n"
                "1. Вимкнути програми фотоапарата та друку\n"
                "2. Вимкнути ноутбук та фотоапарат\n"
                "3. Заправити принтер фарбою\n"
                "4. Поставити точку та павербанки на зарядку\n"
                "5. Прибрати сміття та протерти точку\n"
                "6. Викинути сміття з офісу"
            )

        elif lang == "it":
            await message.answer(
                "🧹 Chiusura turno:\n\n"
                "1. Spegnere programmi fotocamera e stampa\n"
                "2. Spegnere laptop e fotocamera\n"
                "3. Riempire stampante con inchiostro\n"
                "4. Mettere in carica powerbank e punto\n"
                "5. Pulire il punto\n"
                "6. Buttare la spazzatura dell'ufficio"
            )

    # ОТКРЫТИЕ ТОЧКИ
    elif message.text == texts[lang]["opening"]:

        if lang == "ru":
            await message.answer(
                "🌅 Открытие точки:\n\n"
                "1. Проверить заряд павербанков\n"
                "2. Надежно зафиксировать зарядный кабель\n"
                "3. Проверить наличие:\n"
                "- краски\n"
                "- резинок\n"
                "- прищепок\n"
                "- влажных салфеток\n"
                "- дождевика\n"
                "- зонта\n"
                "4. Осмотреть точку на дефекты\n\n"
                "🔥 И в бой!"
            )

        elif lang == "ua":
            await message.answer(
                "🌅 Відкриття точки:\n\n"
                "1. Перевірити заряд павербанків\n"
                "2. Надійно зафіксувати кабель\n"
                "3. Перевірити наявність:\n"
                "- фарби\n"
                "- резинок\n"
                "- прищіпок\n"
                "- серветок\n"
                "- дощовика\n"
                "- парасолі\n"
                "4. Оглянути точку на дефекти\n\n"
                "🔥 Вперед!"
            )

        elif lang == "it":
            await message.answer(
                "🌅 Apertura punto:\n\n"
                "1. Controllare powerbank\n"
                "2. Fissare bene il cavo\n"
                "3. Controllare presenza di:\n"
                "- inchiostro\n"
                "- elastici\n"
                "- mollette\n"
                "- salviette\n"
                "- impermeabile\n"
                "- ombrello\n"
                "4. Controllare il punto\n\n"
                "🔥 Andiamo!"
            )

    # АРЕНДА
    elif message.text == texts[lang]["rent"]:

        if lang == "ru":
            await message.answer(
                "🏠 Аренда офиса:\n"
                "Оплата каждые 2 месяца.\n"
                "Следующая оплата: 01.06"
            )

        elif lang == "ua":
            await message.answer(
                "🏠 Оренда офісу:\n"
                "Оплата кожні 2 місяці.\n"
                "Наступна оплата: 01.06"
            )

        elif lang == "it":
            await message.answer(
                "🏠 Affitto ufficio:\n"
                "Pagamento ogni 2 mesi.\n"
                "Prossimo pagamento: 01.06"
            )

    # КОМАНДА
    elif message.text == texts[lang]["team"]:

        await message.answer(
            "🔥 STREET FRIENDS 🔥\n\n"
            "Егор\n"
            "Лена\n"
            "Аня\n"
            "Марсель\n"
            "Никита\n"
            "Тарас\n"
            "Юля\n"
            "Марічка"
        )

    # НАСТРОЙКИ
    elif message.text == texts[lang]["settings"]:

        await message.answer(
            "⚙️ Чтобы изменить язык — нажмите /start"
        )


async def main():

    print("BOT STARTED")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())