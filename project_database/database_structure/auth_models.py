from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project_database.db import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Researcher(Base):
    __tablename__ = "researchers"

    researcher_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )

    # Current prototype login/register fields
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    password: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    display_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    # Keep lightweight for current phase, but useful for later integration
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="researcher"
    )
    account_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    sessions: Mapped[list["ResearcherSession"]] = relationship(
        "ResearcherSession",
        back_populates="researcher",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Researcher(researcher_id={self.researcher_id}, email={self.email})>"

    @property
    def initial(self) -> str:
        name = (self.display_name or "").strip()
        return (name[:1] or "R").upper()


class ResearcherSession(Base):
    __tablename__ = "researcher_sessions"

    session_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )

    researcher_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("researchers.researcher_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Can be used later to replace current cookie payload with DB-backed session token
    session_token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        default=lambda: str(uuid4()),
        index=True
    )

    issued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: utc_now() + timedelta(hours=8)
    )
    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True
    )
    user_agent: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    researcher: Mapped["Researcher"] = relationship(
        "Researcher",
        back_populates="sessions"
    )

    def __repr__(self) -> str:
        return (
            f"<ResearcherSession(session_id={self.session_id}, "
            f"researcher_id={self.researcher_id}, revoked={self.is_revoked})>"
        )

    @property
    def is_active(self) -> bool:
        return (not self.is_revoked) and (self.expires_at > utc_now())