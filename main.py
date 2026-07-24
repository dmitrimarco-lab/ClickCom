import asyncio
import re
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ВСТАВЬ СЮДА ТОКЕН ОТ BOTFATHER
API_TOKEN = '8986130565:AAG3aPID781InTIAsqmUMvTAFjPPeL_EtNs'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Данные хранятся в памяти
user_stats = {}

def parse_work_message(text: str):
    # Проверяем наличие огонька
    if "🔥" not in text:
        return None

    # Ищем строчку "Стоимость работы: ХХ"
    match = re.search(r"Стоимость работы:\s*([\d\.\,]+)", text, re.IGNORECASE)
    if match:
        val_str = match.group(1).replace(',', '.')
        try:
            return float(val_str)
        except ValueError:
            return None
    return None

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🔥 **Бот учета заявок запущен!**\n\n"
        "Просто пересылай сюда сообщения с выполненными заказами.\n\n"
        "**Команды:**\n"
        "📊 `/stats` — Посмотреть итог за день\n"
        "🔄 `/reset` — Сбросить счетчик (начать новый день/смену)"
    )

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    data = user_stats.get(message.from_user.id, {"count": 0, "total_sum": 0.0})
    await message.answer(
        f"📊 **Статистика:**\n\n"
        f"🔥 Выполнено работ: **{data['count']}**\n"
        f"💰 Общая сумма: **{data['total_sum']:.2f} MDL**"
    )

@dp.message(Command("reset"))
async def cmd_reset(message: types.Message):
    user_stats[message.from_user.id] = {"count": 0, "total_sum": 0.0}
    await message.answer("🔄 Счетчик сброшен! Можно начинать новую смену.")

@dp.message()
async def process_message(message: types.Message):
    if not message.text:
        return

    price = parse_work_message(message.text)
    
    if price is not None:
        uid = message.from_user.id
        if uid not in user_stats:
            user_stats[uid] = {"count": 0, "total_sum": 0.0}

        user_stats[uid]["count"] += 1
        user_stats[uid]["total_sum"] += price

        await message.reply(
            f"✅ **Принято!**\n\n"
            f"➕ Добавлено: **{price}**\n"
            f"🔥 Всего заявок с 🔥: **{user_stats[uid]['count']}**\n"
            f"💵 Итоговая сумма: **{user_stats[uid]['total_sum']:.2f} MDL**"
        )

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
