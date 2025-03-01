from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def get_boost_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Купить буст", callback_data="buy_boost"
                )
            ],
            [
                InlineKeyboardButton(
                    text="В главное меню", callback_data="main_menu"
                )
            ],
        ],
    )
    return keyboard
