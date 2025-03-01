from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from dishka.integrations.aiogram import FromDishka, inject

from tgbot.application import UserGateway
from tgbot.presentation.v2.keyboards import (
    get_get_link_keyboard,
)
from tgbot.presentation.v2.subscribe_check import check_with_answer

get_link_router = Router()


@get_link_router.callback_query(F.data == "get_link")
@inject
async def get_daily_bonus(
    callback: CallbackQuery, session: FromDishka[AsyncSession], bot: Bot
):
    if not await check_with_answer(
        bot=bot,
        message=callback.message,
        user_tg_id=callback.from_user.id,
        session=session,
    ):
        return
    user_gateway = UserGateway(session)
    user = await user_gateway.by_tg_id(callback.from_user.id)
    await callback.message.edit_text(
        text=f"""
        🎉 Приглашай друзей и получай звёзды! ⭐️
🔗 Твоя личная ссылка:
https://t.me/{(await bot.get_me()).username}?start={user.referral_code} # TODO: скопировать залупу


🚀 Как набрать много переходов по ссылке?
• Отправь её друзьям в личные сообщения 👥
• Поделись ссылкой в истории в своем ТГ или в своем Telegram канале 📱
• Оставь её в комментариях или чатах 🗨
• Распространяй ссылку в соцсетях: TikTok, Instagram, WhatsApp и других 🌍

💎 Что ты получишь?
За каждого друга, который перейдет по твоей ссылке и активирует бота, ты получаешь +3⭐️!

Делись и зарабатывай уже сейчас! 🚀
        """,
        reply_markup=get_get_link_keyboard(),
    )
