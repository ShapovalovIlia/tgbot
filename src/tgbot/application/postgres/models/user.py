from sqlalchemy import (
    Column,
    UUID,
    String,
    Boolean,
    Date,
    Integer,
    Float,
    text,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship

from .base import Base
from .user_task import user_task_table


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    tg_id = Column(String, nullable=False, unique=True)
    username = Column(String)
    promo = Column(Boolean, nullable=False)
    daily_bonus = Column(Date, nullable=False)
    referrer = Column(UUID)
    referral_code = Column(String, nullable=False, unique=True)
    amount_of_referrals = Column(Integer, nullable=False, default=0)
    balance = Column(Float, nullable=False)
    earned = Column(Float, nullable=False)
    verify_timestamp = Column(TIMESTAMP)
    # Связь многие-ко-многим через таблицу user_task
    tasks = relationship(
        "Task",
        secondary=user_task_table,
        back_populates="users",
        passive_deletes=True,
    )
