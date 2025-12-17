from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from logger.logs_setting import logger
from models.balance import BalanceState, BalanceOperation


class BalanceRepository:
    @staticmethod
    async def get_or_create(
            session: AsyncSession,
            chat_id: int,
            user_id: int,
    ) -> BalanceState:
        stmt = (
            select(BalanceState)
            .where(
                BalanceState.chat_id == chat_id,
                BalanceState.user_id == user_id,
            )
        )

        result = await session.execute(stmt)
        state = result.scalar_one_or_none()

        if state is None:
            state = BalanceState(
                chat_id=chat_id,
                user_id=user_id,
            )
            session.add(state)
            await session.flush()

        return state

    @staticmethod
    async def apply_delta(
            session: AsyncSession,
            state: BalanceState,
            delta: int,
    ) -> None:
        old_balance = state.balance
        old_checks = state.checks_count

        state.balance += delta

        if delta > 0:
            state.checks_count += 1
        elif delta < 0 < state.checks_count:
            state.checks_count -= 1

        session.add(
            BalanceOperation(
                chat_id=state.chat_id,
                user_id=state.user_id,
                delta=delta,
            )
        )

        await session.commit()

        logger.info(
            "BALANCE_UPDATE | chat_id=%s | user_id=%s | delta=%s | "
            "balance: %s -> %s | checks: %s -> %s",
            state.chat_id,
            state.user_id,
            delta,
            old_balance,
            state.balance,
            old_checks,
            state.checks_count,
        )

    @staticmethod
    async def reset(
            session: AsyncSession,
            state: BalanceState
    ) -> None:
        state.balance = 0
        state.checks_count = 0
        await session.commit()
