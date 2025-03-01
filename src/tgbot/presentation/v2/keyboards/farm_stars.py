from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def get_farm_stars_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Получить звезды", callback_data="farm_click"
                )
            ],
            [InlineKeyboardButton(text="Назад", callback_data="main_menu")],
        ],
    )
    return keyboard
