import os
import asyncio

from aiogram import Bot, Dispatcher
from dishka.integrations.aiogram import setup_dishka

from tgbot.infrastructure import ioc_container_factory
from tgbot.presentation.routers import (
    start_router,
    main_router,
    profile_router,
    rating_router,
    withdraw_router,
    gain_stars_router,
    tasks_router,
)


async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(main_router)
    dp.include_router(profile_router)
    dp.include_router(rating_router)
    dp.include_router(withdraw_router)
    dp.include_router(gain_stars_router)
    dp.include_router(tasks_router)

    container = ioc_container_factory()
    setup_dishka(container=container, router=dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
