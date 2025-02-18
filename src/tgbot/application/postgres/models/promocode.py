from .base import Base

from sqlalchemy import Column, UUID, String, text, Float, Integer


class Promocode(Base):
    __tablename__ = "promocodes"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    name = Column(String, nullable=False, unique=True)
    remaining_usages = Column(Integer, nullable=False)
    reward = Column(Float, nullable=False)
