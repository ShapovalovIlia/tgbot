from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.filters.callback_data import CallbackData

from tgbot.application import Task


class TaskCallback(CallbackData, prefix="task"):
    tg_id: int


def get_subscribe_task_keyboard(task: Task):
    keyboard = []
    keyboard.append(
        [
            InlineKeyboardButton(
                text=f"Канал спонсора",
                url=task.link,
            )
        ]
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                text="Проверить подписку",
                callback_data=TaskCallback(tg_id=int(task.tg_id)).pack(),
            )
        ]
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                text="В главное меню",
                callback_data="main_menu",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
