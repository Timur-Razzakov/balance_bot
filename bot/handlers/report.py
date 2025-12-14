from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message

from logger.logs_setting import logger
from repositories.balance_report_repository import BalanceReportRepository
from utils.formatters import format_money

router = Router()


@router.message(F.text == "📊 Отчёт")
@router.message(F.text == "/report")
async def report_handler(message: Message, session_maker):
    user_id = message.from_user.id

    logger.info(
        "REPORT_REQUEST | user_id=%s",
        user_id,
    )
    async with session_maker() as session:
        repo = BalanceReportRepository()
        rows = await repo.report_by_days(session, message.from_user.id)

    if not rows:
        logger.info(
            "REPORT_EMPTY | user_id=%s",
            user_id,
        )
        await message.answer("📭 Пока нет данных для отчёта.")
        return
    logger.info(
        "REPORT_SUCCESS | user_id=%s | days=%s",
        user_id,
        len(rows),
    )
    text = "📊 <b>Отчёт по дням</b>\n\n"

    for day, total, checks in rows:
        pretty_day = datetime.strptime(str(day), "%Y-%m-%d").strftime("%d %B %Y")

        text += (
            f"📅 <b>{pretty_day}</b>\n"
            f"💰 <b>{format_money(total)}</b>\n"
            f"🧾 Чеков: <b>{checks}</b>\n"
            f"━━━━━━━━━━━━━━━\n"
        )

    await message.answer(text, parse_mode="HTML")
