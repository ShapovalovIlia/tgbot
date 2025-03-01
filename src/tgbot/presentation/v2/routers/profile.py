from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dishka.integrations.aiogram import FromDishka, inject

from tgbot.application import UserGateway
from tgbot.presentation.v2.keyboards import (
    get_profile_keyboard,
)
from tgbot.presentation.v2.subscribe_check import check_with_answer

profile_router = Router()


@profile_router.callback_query(F.data == "profile")
@inject
async def profile(
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
        ✨ Профиль

👤 Имя: {callback.from_user.first_name}
🆔 ID: {callback.from_user.id}

👥 Всего друзей: todo
📆 Активировали бота: {user.amount_of_referrals}
🔄 Баланс {user.balance}

📌 Используй кнопки ниже для действий.
        """,
        reply_markup=get_profile_keyboard(),
    )


class PromoCodeState(StatesGroup):
    waiting_for_promo = State()


# @profile_router.callback_query(F.data == "promo")
# @inject
# async def enter_promo_code(
#     callback: CallbackQuery, session: FromDishka[AsyncSession], bot: Bot, state: FSMContext,
# ):
#     if not await check_with_answer(
#         bot=bot,
#         message=callback.message,
#         session=session,
#         user_tg_id=callback.from_user.id,
#     ):
#         return

#     user_gateway = UserGateway(session=session)
#     user = await user_gateway.by_tg_id(callback.from_user.id)

#     if user.promo:
#         await callback.answer(
#             "Вы уже вводили промокод", show_alert=True
#         )

#     else:
#         await callback.message.answer(
#             "Введите ваш промокод", reply_markup=get_back_keyboard()
#         )
#         await state.set_state(PromoCodeState.waiting_for_promo)


# @profile_router.callback_query(PromoCodeState.waiting_for_promo)
# @inject
# async def process_promo_code(
#     message: Message,
#     state: FSMContext,
#     session: FromDishka[AsyncSession],
#     bot: Bot,
# ):
#     if not await check_with_answer(bot=bot, message=message, session=session):
#         return

#     # Если текст сообщения отсутствует.
#     if not message.text:
#         await message.answer("Некорректное сообщение. Попробуйте ещё раз.")
#         return

#     # Обработка команды "Назад"
#     if message.text == "Назад":
#         await message.answer(
#             "🔝 Главное Меню", reply_markup=get_main_keyboard()
#         )
#         await state.clear()
#         return

#     # Ищем промокод в базе данных
#     promo = await session.scalar(
#         select(Promocode).where(Promocode.name == message.text)
#     )
#     if not promo:
#         await message.answer("Такого промокода не существует")
#         return

#     # Проверяем, есть ли оставшиеся использования промокода
#     if promo.remaining_usages <= 0:
#         await message.answer("Этот промокод больше недействителен")
#         return

#     # Обновляем данные промокода
#     promo.remaining_usages -= 1

#     # Ищем пользователя по его Telegram ID
#     user = await session.scalar(
#         select(User).where(User.tg_id == str(message.from_user.id))
#     )
#     if not user:
#         await message.answer("Пользователь не найден")
#         return

#     # Начисляем вознаграждение пользователю
#     user.balance += promo.reward
#     user.earned += promo.reward
#     user.promo = True

#     # Фиксируем изменения в базе
#     await session.commit()
#     await state.clear()

#     # Сообщаем пользователю об успешном применении промокода
#     await message.answer(
#         f"Вы ввели промокод: {message.text}\nПромокод принят!\nВам начислено - {promo.reward} звед",
#         reply_markup=get_main_keyboard(),
#     )
