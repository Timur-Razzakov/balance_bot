from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.balance import BalanceOperation


class BalanceReportRepository:

    async def report_by_days(
        self,
        session: AsyncSession,
        user_id: int,
    ):
        stmt = (
            select(
                func.date(BalanceOperation.created_at).label("day"),
                func.sum(BalanceOperation.delta).label("total"),
                func.count()
                .filter(BalanceOperation.delta > 0)
                .label("checks"),
            )
            .where(BalanceOperation.user_id == user_id)
            .group_by(func.date(BalanceOperation.created_at))
            .order_by(func.date(BalanceOperation.created_at))
        )

        result = await session.execute(stmt)
        return result.all()
