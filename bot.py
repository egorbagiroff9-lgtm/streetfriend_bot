import asyncio
import os
from datetime import datetime

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
# КОМАНДЫ ТОЛЬКО В ЛС
# =========================================

def is_private(message: types.Message):

    return message.chat.type == "private"
    
# =========================================
# ПРОВЕРКА АДМИНА
# =========================================

def is_admin(message: types.Message):

    return message.from_user.id == ADMIN_ID
# =========================================
# МОЙ ID
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

    # Игнорируем группы
    if not is_private(message):
        return

    await message.answer(

        "🔥 STREET FRIENDS BOT\n\n"

        "Бот работает как система напоминаний для команды ❤️\n\n"

        "Доступные команды:\n\n"

        "/team — команда\n"
        "/duty — дежурные\n"
        "/setduty — сменить дежурных\n"
        "/restart — перезапуск\n"
    )

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
# КОМАНДА
# =========================================

@dp.message(Command("team"))
async def team(message: types.Message):

    if not is_private(message):
        return

    team_text = "\n".join(
        [f"• {name}" for name in TEAM]
    )

    await message.answer(
        f"👥 STREET FRIENDS TEAM\n\n{team_text}"
    )

# =========================================
# ДЕЖУРНЫЕ
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
# СМЕНА ДЕЖУРНЫХ
# =========================================

@dp.message(Command("setduty"))
async def set_duty(message: types.Message):

    if not is_private(message):
        return

    # Только админ
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

    people = text.split()

    office_duty = people

    duty_text = "\n".join(
        [f"• {name}" for name in office_duty]
    )

    await message.answer(

        "✅ Новые дежурные:\n\n"

        f"{duty_text}"
    )
# =========================================
# СПИСОК КОМАНД
# =========================================

@dp.message(Command("help"))
async def help_command(message: types.Message):

    # Команды для всех
    user_commands = (
        "👥 ДОСТУПНЫЕ КОМАНДЫ\n\n"

        "/start — запуск бота\n"
        "/restart — перезапуск\n"
        "/help — список команд\n\n"

        "📌 Основные разделы:\n"
        "• ☀️ Открытие точки\n"
        "• 🧹 Закрытие точки\n"
        "• 💰 Общак\n"
        "• 🏠 Аренда\n"
        "• 📅 Смены\n"
        "• 👥 Команда\n"
        "• 📍 Точки\n"
        "• 🎉 Фесты\n"
    )

    # Если админ → показываем админ команды
    if is_admin(message):

        admin_commands = (
            "\n⚙️ АДМИН КОМАНДЫ\n\n"

            "/announce текст\n"
            "→ отправить объявление в группу\n\n"

            "Пример:\n"
            "/announce Завтра сбор в 09:00 🔥"
        )

        await message.answer(
            user_commands + admin_commands
        )

    else:

        await message.answer(
            user_commands
        )
# =========================================
# АВТОНАПОМИНАНИЯ
# =========================================
# =========================================
# ОБЪЯВЛЕНИЕ В ГРУППУ
# =========================================

@dp.message(Command("announce"))
async def announce(message: types.Message):

    # Только ЛС
    if not is_private(message):
        return

    # Только админ
    if not is_admin(message):

        await message.answer(
            "❌ Только администратор"
        )

        return

    # Получаем текст объявления
    text = message.text.replace(
        "/announce",
        ""
    ).strip()

    # Если текста нет
    if not text:

        await message.answer(

            "❌ Пример:\n\n"

            "/announce Завтра сбор в 09:00"
        )

        return

    # Отправляем объявление в группу
    await bot.send_message(

        GROUP_ID,

        "📢 STREET FRIENDS\n\n"

        f"{text}"
    )

    # Подтверждение админу
    await message.answer(
        "✅ Объявление отправлено"
    )
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

                "1. Проверить заряд павербанков 🔋\n"
                "2. Проверить кабель питания 🔌\n"
                "3. Проверить расходники 📦\n"
                "4. Осмотреть ТОЧКУ 👀\n\n"

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
            now.weekday() == 6 and
            now.hour == 12 and
            now.minute == 0
        ):

            await bot.send_message(
                GROUP_ID,

                "💰 STREET FRIENDS\n\n"

                "Напоминание:\n\n"

                "Сегодня каждый участник кладет 25€ в ОБЩАК ❤️"
            )

        # =====================================
        # УБОРКА ОФИСА
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
            now.day == 1 and
            now.month in [2, 4, 6, 8, 10, 12] and
            now.hour == 12 and
            now.minute == 0
        ):

            await bot.send_message(
                GROUP_ID,

                "🏠 STREET FRIENDS\n\n"

                "Напоминание:\n\n"

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