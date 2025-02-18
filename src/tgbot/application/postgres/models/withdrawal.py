from sqlalchemy import Column, ForeignKey, Table, UUID, Float

from .base import Base


withdrawl_requests = Table(
    "withdrawl_requests",
    Base.metadata,
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "amount",
        Float,
        nullable=False,
    ),
)
