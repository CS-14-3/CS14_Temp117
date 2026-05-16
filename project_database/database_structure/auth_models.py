from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project_database.db import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Researcher(Base):
    __tablename__ = "researchers"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    surveys: Mapped[list["Survey"]] = relationship(
        "Survey",
        back_populates="researcher",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Researcher(id={self.id}, username={self.username})>"
