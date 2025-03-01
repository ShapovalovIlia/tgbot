from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def get_reviews_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="main_menu")],
        ],
    )
    return keyboard
