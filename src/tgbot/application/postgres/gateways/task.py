from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from tgbot.application.postgres.models import Task


class TaskGateway:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def by_tg_id(self, tg_id: int) -> Task | None:
        task = await self._session.scalar(
            select(Task).where(Task.tg_id == str(tg_id))
        )
        return task
