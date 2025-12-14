from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            # KeyboardButton(text="📊 Отчёт"),
            KeyboardButton(text="🔄 Сброс"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)
