from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def get_profile_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Промокод", callback_data="promo"),
                InlineKeyboardButton(text="Ежедневка", callback_data="daily"),
            ],
            [
                InlineKeyboardButton(
                    text="В главное меню", callback_data="main_menu"
                )
            ],
        ],
    )
    return keyboard


# def get_promo_keyboard
