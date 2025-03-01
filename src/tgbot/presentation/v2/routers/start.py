from datetime import date, timedelta, datetime

from dishka.integrations.aiogram import inject, FromDishka

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject

from tgbot.presentation.v2.keyboards import (
    get_main_keyboard,
    get_initial_keyboard,
)
from tgbot.presentation.v2.subscribe_check import (
    check_with_answer,
)
from tgbot.application import User, UserGateway, SponsorGateway

start_router = Router()


@start_router.message(CommandStart())
@inject
async def start_handler(
    message: Message, command: CommandObject, session: FromDishka[AsyncSession]
):
    user_gateway = UserGateway(session)
    sponsor_gateway = SponsorGateway(session)
    sponsors = await sponsor_gateway.all_sponsors()
    user = await user_gateway.by_tg_id(message.from_user.id)

    if not user:
        referral_code = command.args
        referrer = None
        if referral_code:
            referrer = await user_gateway.by_referral_code(referral_code)

        user = User(
            tg_id=str(message.from_user.id),
            promo=False,
            daily_bonus=date.today() - timedelta(days=1),
            referrer=referrer.id if referrer else None,
            referral_code=str(message.from_user.id),
            balance=0,
            earned=0,
            verify_timestamp=None,
            username=message.from_user.first_name,
        )

        session.add(user)
        await session.commit()

    await message.answer(
        text="""
        Привет, чтобы активировать бота и начать получать ⭐️ звезды за друзей:
1️⃣ Подпишись на наших спонсоров (это займет 5 секунд).
2️⃣ Нажми "Проверить подписку ✅
        """,
        reply_markup=get_initial_keyboard(sponsors),
    )


@start_router.callback_query(F.data == "check_subscription")
@inject
async def check_user_subscription_callback_answer(
    callback: CallbackQuery, bot: Bot, session: FromDishka[AsyncSession]
):
    if not await check_with_answer(
        bot=bot,
        message=callback.message,
        session=session,
        user_tg_id=callback.from_user.id,
    ):
        return

    user_tg_id = callback.from_user.id
    user_gateway = UserGateway(session)
    user = await user_gateway.by_tg_id(user_tg_id)

    if not user.verify_timestamp:
        user.verify_timestamp = datetime.now()
        if user.referrer is not None:
            referrer = await session.scalar(
                select(User).where(User.id == str(user.referrer))
            )
            if referrer:
                referrer.balance += 2.5
                referrer.earned += 2.5
                referrer.amount_of_referrals += 1
                # await send_notification(
                #     chat_id=referrer.tg_id,
                #     message=f"По вашей реферальной ссылке зарегестрирован пользователь, вам начислена награда в размере 2.5 ✨",
                #     bot=bot,
                # )

        await session.commit()

    await callback.answer("✅ Вы подписаны на все каналы!", show_alert=True)

    await callback.message.edit_text(
        text=f"""
        главное меню
        """,
        reply_markup=get_main_keyboard(),
    )
