from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from logger.logs_setting import logger
from repositories.balance import BalanceRepository
from utils.formatters import format_money

router = Router()
repo = BalanceRepository()


def is_number(text: str) -> bool:
    return text.lstrip("-").isdigit()


@router.message(F.text == "🔄 Сброс")
@router.message(F.text == "/end")
async def reset(message: Message, session_maker):
    user_id = message.from_user.id
    chat_id = message.chat.id

    async with session_maker() as session:
        state = await repo.get_or_create(
            session=session,
            chat_id=chat_id,
            user_id=user_id,
        )

        logger.info(
            "RESET | chat_id=%s | user_id=%s | balance_before=%s | checks_before=%s",
            chat_id,
            user_id,
            state.balance,
            state.checks_count,
        )

        text = (
            f"📅 {datetime.now().strftime('%d.%m.%Y')}\n"
            f"💰 Итоговая сумма: {format_money(state.balance)}\n"
            f"🧾 Чеков: {state.checks_count}"
        )

        await message.answer(text)
        await repo.reset(session, state)

        logger.info(
            "RESET_DONE | chat_id=%s | user_id=%s | balance_after=0 | checks_after=0",
            chat_id,
            user_id,
        )


@router.message(F.text.regexp(r"^-?\d+$"))
async def handle_amount(message: Message, session_maker):
    raw = message.text.replace(" ", "")
    value = int(raw)

    user_id = message.from_user.id
    chat_id = message.chat.id
    async with session_maker() as session:
        state = await repo.get_or_create(
            session=session,
            chat_id=chat_id,
            user_id=user_id,
        )
        balance_before = state.balance
        checks_before = state.checks_count

        await repo.apply_delta(session, state, value)

        if value > 0:
            header = f"✅ Баланс пополнен на {format_money(value)}"
        else:
            header = f"➖ Баланс уменьшен на {format_money(abs(value))}"

        text = (
            f"{header}\n\n"
            f"💰 Текущий баланс: {format_money(state.balance)}\n"
            f"🧾 Чеков: {state.checks_count}"
        )

        logger.info(
            "APPLY_DELTA | chat_id=%s | user_id=%s | delta=%s | "
            "balance: %s -> %s | checks: %s -> %s",
            chat_id,
            user_id,
            value,
            balance_before,
            state.balance,
            checks_before,
            state.checks_count,
        )

        await message.answer(text)
