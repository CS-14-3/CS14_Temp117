from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project_database.db import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ParticipantSession(Base):
    __tablename__ = "participant_sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )
    publication_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("survey_publications.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="started"
    )
    gaze_data_json: Mapped[dict | list | None] = mapped_column(
        JSON,
        nullable=True
    )

    publication: Mapped["SurveyPublication"] = relationship(
        "SurveyPublication",
        back_populates="participant_sessions"
    )
    answers: Mapped[list["ParticipantAnswer"]] = relationship(
        "ParticipantAnswer",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ParticipantSession(id={self.id}, publication_id={self.publication_id}, status={self.status})>"


class ParticipantAnswer(Base):
    __tablename__ = "participant_answers"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )
    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("participant_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    news_item_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("survey_news_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    variant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("survey_variants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    option_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("survey_question_options.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    answered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    session: Mapped["ParticipantSession"] = relationship(
        "ParticipantSession",
        back_populates="answers"
    )
    news_item: Mapped["SurveyNewsItem"] = relationship(
        "SurveyNewsItem",
        back_populates="participant_answers"
    )
    variant: Mapped["SurveyVariant"] = relationship(
        "SurveyVariant",
        back_populates="participant_answers"
    )
    option: Mapped["SurveyQuestionOption"] = relationship(
        "SurveyQuestionOption",
        back_populates="participant_answers"
    )

    def __repr__(self) -> str:
        return (
            f"<ParticipantAnswer(id={self.id}, session_id={self.session_id}, "
            f"variant_id={self.variant_id}, option_id={self.option_id})>"
        )
