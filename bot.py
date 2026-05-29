import asyncio
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# =========================================
# НАСТРОЙКИ
# =========================================

GROUP_ID = -1003462381248
ADMIN_ID = 350469503

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

office_duty = [
    "Егор",
    "Лена",
]

# =========================================
# СОСТОЯНИЯ
# =========================================

waiting_announce = {}

# =========================================
# ПРОВЕРКИ
# =========================================

def is_private(message: types.Message):

    return message.chat.type == "private"


def is_admin(message: types.Message):

    return message.from_user.id == ADMIN_ID

# =========================================
# КНОПКИ
# =========================================

admin_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(
                text="📢 Анонс"
            )
        ],
        [
            types.KeyboardButton(
                text="👥 Команда"
            ),
            types.KeyboardButton(
                text="🧹 Дежурные"
            )
        ],
        [
            types.KeyboardButton(
                text="⚙️ Команды"
            )
        ]
    ],
    resize_keyboard=True
)

user_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(
                text="👥 Команда"
            ),
            types.KeyboardButton(
                text="🧹 Дежурные"
            )
        ],
        [
            types.KeyboardButton(
                text="⚙️ Команды"
            )
        ]
    ],
    resize_keyboard=True
)

# =========================================
# /MYID
# =========================================

@dp.message(Command("myid"))
async def myid(message: types.Message):

    await message.answer(
        f"🆔 Твой ID:\n\n{message.from_user.id}"
    )

# =========================================
# /START
# =========================================

@dp.message(Command("start"))
async def start(message: types.Message):

    if not is_private(message):
        return

    # Админ
    if is_admin(message):

        await message.answer(

            "🔥 STREET FRIENDS BOT\n\n"

            "Ты вошел как администратор ⚙️\n\n"

            "Доступна кнопка анонсов.",

            reply_markup=admin_keyboard
        )

    # Пользователь
    else:

        await message.answer(

            "🔥 STREET FRIENDS BOT\n\n"

            "Бот работает как система "
            "напоминаний ❤️",

            reply_markup=user_keyboard
        )

# =========================================
# /HELP
# =========================================

@dp.message(Command("help"))
async def help_command(message: types.Message):

    if not is_private(message):
        return

    text = (

        "👥 ДОСТУПНЫЕ КОМАНДЫ\n\n"

        "/start — запуск бота\n"
        "/restart — перезапуск\n"
        "/help — список команд\n"
        "/team — команда\n"
        "/duty — дежурные\n\n"

        "📌 Автонапоминания:\n"
        "• открытие точки\n"
        "• закрытие точки\n"
        "• уборка офиса\n"
        "• аренда\n"
        "• общак\n"
    )

    if is_admin(message):

        text += (

            "\n⚙️ АДМИН КОМАНДЫ\n\n"

            "/announce — объявление\n"
            "/setduty — смена дежурных\n\n"

            "Пример:\n"
            "/setduty Егор Юля"
        )

    await message.answer(text)

# =========================================
# /RESTART
# =========================================

@dp.message(Command("restart"))
async def restart(message: types.Message):

    if not is_private(message):
        return

    await message.answer(
        "🔄 Бот успешно перезапущен"
    )

# =========================================
# /TEAM
# =========================================

@dp.message(Command("team"))
async def team(message: types.Message):

    if not is_private(message):
        return

    team_text = "\n".join(
        [f"• {name}" for name in TEAM]
    )

    await message.answer(

        "👥 STREET FRIENDS TEAM\n\n"

        f"{team_text}"
    )

# =========================================
# /DUTY
# =========================================

@dp.message(Command("duty"))
async def duty(message: types.Message):

    if not is_private(message):
        return

    duty_text = "\n".join(
        [f"• {name}" for name in office_duty]
    )

    await message.answer(

        "🧹 ДЕЖУРНЫЕ ПО ОФИСУ\n\n"

        f"{duty_text}"
    )

# =========================================
# /SETDUTY
# =========================================

@dp.message(Command("setduty"))
async def set_duty(message: types.Message):

    if not is_private(message):
        return

    if not is_admin(message):

        await message.answer(
            "❌ Только администратор"
        )

        return

    global office_duty

    text = message.text.replace(
        "/setduty",
        ""
    ).strip()

    if not text:

        await message.answer(

            "❌ Пример:\n\n"

            "/setduty Егор Юля"
        )

        return

    office_duty = text.split()

    duty_text = "\n".join(
        [f"• {name}" for name in office_duty]
    )

    await message.answer(

        "✅ Новые дежурные:\n\n"

        f"{duty_text}"
    )

# =========================================
# /ANNOUNCE
# =========================================

@dp.message(Command("announce"))
async def announce(message: types.Message):

    if not is_private(message):
        return

    if not is_admin(message):

        await message.answer(
            "❌ Только администратор"
        )

        return

    waiting_announce[
        message.from_user.id
    ] = True

    await message.answer(

        "📢 Введите текст объявления.\n\n"

        "Следующее сообщение будет "
        "отправлено в группу 🔥"
    )

# =========================================
# КНОПКИ
# =========================================

@dp.message()
async def buttons(message: types.Message):

    if not is_private(message):
        return

    # =====================================
    # КНОПКА АНОНСА
    # =====================================

    if (
        is_admin(message)
        and
        message.text == "📢 Анонс"
    ):

        waiting_announce[
            message.from_user.id
        ] = True

        await message.answer(

            "📢 Отправь текст объявления.\n\n"

            "Следующее сообщение "
            "улетит в группу 🔥"
        )

        return

    # =====================================
    # ОБРАБОТКА АНОНСА
    # =====================================

    if waiting_announce.get(
        message.from_user.id
    ):

        waiting_announce[
            message.from_user.id
        ] = False

        await bot.send_message(

            GROUP_ID,

            "📢 STREET FRIENDS\n\n"

            f"{message.text}"
        )

        await message.answer(
            "✅ Объявление отправлено"
        )

        return

    # =====================================
    # КОМАНДА
    # =====================================

    if message.text == "👥 Команда":

        team_text = "\n".join(
            [f"• {name}" for name in TEAM]
        )

        await message.answer(

            "👥 STREET FRIENDS TEAM\n\n"

            f"{team_text}"
        )

    # =====================================
    # ДЕЖУРНЫЕ
    # =====================================

    elif message.text == "🧹 Дежурные":

        duty_text = "\n".join(
            [f"• {name}" for name in office_duty]
        )

        await message.answer(

            "🧹 ДЕЖУРНЫЕ ПО ОФИСУ\n\n"

            f"{duty_text}"
        )

    # =====================================
    # КОМАНДЫ
    # =====================================

    elif message.text == "⚙️ Команды":

        text = (

            "👥 ДОСТУПНЫЕ КОМАНДЫ\n\n"

            "/start\n"
            "/restart\n"
            "/help\n"
            "/team\n"
            "/duty\n"
        )

        if is_admin(message):

            text += (

                "\n⚙️ АДМИН\n\n"

                "/announce\n"
                "/setduty"
            )

        await message.answer(text)



# =========================================
# АВТОНАПОМИНАНИЯ
# =========================================

last_trigger = set()

async def auto_reminders():

    while True:

        now = datetime.now(
            ZoneInfo("Europe/Rome")
        )

        current = now.strftime(
            "%Y-%m-%d %H:%M"
        )

        # =====================================
        # ОТКРЫТИЕ ТОЧКИ
        # =====================================

        if (
            now.hour == 9
            and now.minute == 0
            and current not in last_trigger
        ):

            last_trigger.add(current)

            await bot.send_message(

                GROUP_ID,

                "☀️ STREET FRIENDS\n\n"

                "Напоминание об открытии ТОЧКИ:\n\n"

                "1. Проверить заряд павербанков 🔋\n"
                "2. Проверить кабель питания 🔌\n"
                "3. Проверить расходники 📦\n"
                "4. Осмотреть ТОЧКУ 👀\n\n"

                "🔥 Хорошей работы!"
            )

        # =====================================
        # ЗАКРЫТИЕ ТОЧКИ
        # =====================================

        if (
            now.hour == 20
            and now.minute == 45
            and current not in last_trigger
        ):

            last_trigger.add(current)

            await bot.send_message(

                GROUP_ID,

                "🌙 STREET FRIENDS\n\n"

                "Напоминание о закрытии ТОЧКИ:\n\n"

                "1. Выключить программы 📸\n"
                "2. Выключить ноутбук 💻\n"
                "3. Зарядить ТОЧКУ 🔋\n"
                "4. Зарядить павербанки 🔌\n"
                "5. Убрать мусор 🧹\n"
                "6. Протереть ТОЧКУ ✨"
            )

        # =====================================
        # ОБЩАК
        # =====================================

        if (
            now.weekday() == 6
            and now.hour == 12
            and now.minute == 0
            and current not in last_trigger
        ):

            last_trigger.add(current)

            await bot.send_message(

                GROUP_ID,

                "💰 STREET FRIENDS\n\n"

                "Сегодня каждый участник "
                "кладет 25€ в ОБЩАК ❤️"
            )

        # =====================================
        # УБОРКА ОФИСА
        # =====================================

        if (
            now.weekday() == 3
            and now.hour == 12
            and now.minute == 0
            and current not in last_trigger
        ):

            last_trigger.add(current)

            duty_text = "\n".join(
                [f"• {name}" for name in office_duty]
            )

            await bot.send_message(

                GROUP_ID,

                "🧹 STREET FRIENDS\n\n"

                "Напоминание про уборку офиса:\n\n"

                f"{duty_text}\n\n"

                "Что нужно сделать:\n\n"

                "• подмести офис\n"
                "• вынести мусор\n"
                "• протереть поверхности\n"
                "• проверить зарядки\n"
                "• навести порядок ❤️"
            )

        # =====================================
        # АРЕНДА
        # =====================================

        if (
            now.day == 1
            and now.month in [2, 4, 6, 8, 10, 12]
            and now.hour == 12
            and now.minute == 0
            and current not in last_trigger
        ):

            last_trigger.add(current)

            await bot.send_message(

                GROUP_ID,

                "🏠 STREET FRIENDS\n\n"

                "Сегодня оплата аренды офиса 💸"
            )

        await asyncio.sleep(20)

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