from .base import Base

from sqlalchemy import Column, UUID, text, String


class Sponsor(Base):
    __tablename__ = "sponsors"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    tg_id = Column(String, nullable=False, unique=True)
    link = Column(String, nullable=False, unique=True)
