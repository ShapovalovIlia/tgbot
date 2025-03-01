from typing import Sequence

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from tgbot.application import Sponsor


def get_initial_keyboard(sponsors: Sequence[Sponsor]):
    keyboard = []
    for i in range(len(sponsors)):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"Спонсор {i + 1}",
                    url=sponsors[i].link,
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                text="Проверить подписку", callback_data="check_subscription"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
