from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✨ Фармить звёзды", callback_data="farm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔗 Получить ссылку",
                    callback_data="get_link",
                )
            ],
            [
                InlineKeyboardButton(
                    text="👤 Профиль", callback_data="profile"
                ),
                InlineKeyboardButton(
                    text="🔄 Обменять звёзды", callback_data="change_stars"
                ),
            ],
            [
                InlineKeyboardButton(text="📜 Задания", callback_data="tasks"),
                InlineKeyboardButton(
                    text="📘 Гайды | FAQ", callback_data="faq"
                ),
            ],
            [
                InlineKeyboardButton(text="🚀 Буст", callback_data="boost"),
                InlineKeyboardButton(
                    text="🎮 Мини-игры", callback_data="mini_games"
                ),
            ],
            [
                InlineKeyboardButton(text="🏆 Топ", callback_data="rating"),
                InlineKeyboardButton(text="❤️ Отзывы", url="t.me/durovv"),
            ],
        ],
    )
    return keyboard
