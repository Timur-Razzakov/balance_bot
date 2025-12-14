import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.handlers import start_router, balance_router, report_router
from data.config import BOT_TOKEN, DB_URL
from db.engine import create_async_engine
from db.session import get_session_maker
from middlewares.admin_only import AdminOnlyMiddleware

logging.basicConfig(level=logging.INFO)


async def main():
    logging.info("🚀 Bot starting...")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.message.middleware(AdminOnlyMiddleware())
    dp.callback_query.middleware(AdminOnlyMiddleware())
    dp.include_router(start_router)
    dp.include_router(balance_router)
    # dp.include_router(report_router)


    # подключаемся к БД
    engine = create_async_engine(DB_URL)
    session_maker = get_session_maker(engine)

    dp["session_maker"] = session_maker

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
