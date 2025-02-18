from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.application.postgres.models import user_task_table


class UserTaskGateway:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, task_id: int, user_id: int) -> None:
        stmt = insert(user_task_table).values(user_id=user_id, task_id=task_id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def by_user_task(self, task_id: int, user_id: int) -> dict | None:
        """Получает запись по user_id и task_id"""
        stmt = select(user_task_table).where(
            user_task_table.c.user_id == user_id,
            user_task_table.c.task_id == task_id,
        )
        result = await self._session.execute(stmt)
        row = result.fetchone()

        if row:
            return dict(row._mapping)  # Преобразуем в словарь
        return None
