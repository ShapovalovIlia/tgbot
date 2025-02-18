from sqlalchemy import Column, ForeignKey, Table, UUID

from .base import Base


user_task_table = Table(
    "user_task",
    Base.metadata,
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "task_id",
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)
