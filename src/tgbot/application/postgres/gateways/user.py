from uuid import UUID
from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.application.postgres.models import User, Task, user_task_table


class UserGateway:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def by_tg_id(self, tg_id: int) -> User | None:
        user = await self._session.scalar(
            select(User).where(User.tg_id == str(tg_id))
        )
        return user

    async def by_referral_code(self, referral_code: str) -> User | None:
        user = await self._session.scalar(
            select(User).where(User.referral_code == referral_code)
        )
        return user

    async def top_referrals_all_time(self) -> Sequence[User]:
        users = (
            await self._session.execute(
                select(User)
                .order_by(User.amount_of_referrals.desc())
                .limit(10)
            )
        ).scalars()

        return users

    async def top_referrals_last_day(self) -> Sequence[User]:
        last_24_hours = datetime.now() - timedelta(
            days=1
        )  # UTC-время за последние 24 часа

        inviter = aliased(
            User
        )  # Алиас для пригласившего пользователя (родителя)
        referral = aliased(User)  # Алиас для реферала (дочернего пользователя)

        result = (
            await self._session.execute(
                select(
                    inviter,  # Выбираем пригласившего пользователя
                    func.count(referral.id).label(
                        "new_referrals"
                    ),  # Считаем новых рефералов
                )
                .select_from(
                    inviter
                )  # Явно указываем, с какой таблицы начинаем
                .join(
                    referral, referral.referrer == inviter.id
                )  # Соединяем пользователей по `referrer`
                .where(
                    referral.verify_timestamp >= last_24_hours
                )  # Только рефералы за последние 24 часа
                .group_by(
                    inviter.id
                )  # Группируем по пригласившему пользователю
                .order_by(
                    func.count(referral.id).desc()
                )  # Сортируем по количеству новых рефералов
                .limit(10)  # Берём топ-10
            )
        ).all()

        return result

    async def last_day_referrals_amount(self, tg_id: int) -> int:
        tg_id = str(tg_id)
        stmt = select(User).where(User.tg_id == tg_id)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return 0

        one_day_ago = datetime.now() - timedelta(days=1)

        count_stmt = select(func.count(User.id)).where(
            User.referrer == user.id, User.verify_timestamp >= one_day_ago
        )
        count_result = await self._session.execute(count_stmt)
        invited_count = count_result.scalar_one()
        return invited_count

    async def tasks_for_user(self, user_id: UUID) -> Sequence[Task] | None:
        stmt = select(Task).where(
            ~Task.id.in_(
                select(user_task_table.c.task_id).where(
                    user_task_table.c.user_id == user_id
                )
            )
        )
        result = await self._session.execute(stmt)
        not_completed_tasks = result.scalars().all()

        return not_completed_tasks

    # async def complete_task(self, user_id: UUID) -> Sequence
