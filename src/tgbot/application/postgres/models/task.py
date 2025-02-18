from sqlalchemy import Column, UUID, String, text, Float
from sqlalchemy.orm import relationship

from .base import Base
from .user_task import user_task_table


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    tg_id = Column(String, nullable=False, unique=True)
    link = Column(String, nullable=False, unique=True)
    description = Column(String)
    reward = Column(Float, nullable=False)

    # Обратная часть связи многие-ко-многим
    users = relationship(
        "User",
        secondary=user_task_table,
        back_populates="tasks",
        passive_deletes=True,
    )
