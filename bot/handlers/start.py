from aiogram import Router, F
from aiogram.types import Message

from bot.keyboards import main_keyboard

router = Router()

@router.message(F.text == "/start")
@router.message(F.text == "▶️ Старт")
async def start(message: Message):
    await message.answer(
        "Вводи сумму:\n"
        "500000 — прибавить\n"
        "-200000 — отнять\n\n"
        "📊 Отчёт — показать статистику\n"
        "🔄 Сброс — показать итог и обнулить",
        reply_markup=main_keyboard,
    )