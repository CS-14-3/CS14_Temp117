from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project_database.db import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Participant(Base):
    __tablename__ = "participants"

    participant_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )

    participant_code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    study_sessions: Mapped[list["StudySession"]] = relationship(
        "StudySession",
        back_populates="participant",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Participant(participant_id={self.participant_id}, participant_code={self.participant_code})>"


class StudySession(Base):
    __tablename__ = "study_sessions"

    study_session_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )

    participant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("participants.participant_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    survey_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("surveys.survey_id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    invite_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        index=True
    )

    session_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="started"
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    calibration_started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    calibration_completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    study_started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    study_ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    exported_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
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

    participant: Mapped["Participant"] = relationship(
        "Participant",
        back_populates="study_sessions"
    )

    survey = relationship("Survey")

    interaction_logs: Mapped[list["ParticipantInteractionLog"]] = relationship(
        "ParticipantInteractionLog",
        back_populates="study_session",
        cascade="all, delete-orphan"
    )

    calibration_results: Mapped[list["CalibrationResult"]] = relationship(
        "CalibrationResult",
        back_populates="study_session",
        cascade="all, delete-orphan"
    )

    gaze_records: Mapped[list["GazeRecord"]] = relationship(
        "GazeRecord",
        back_populates="study_session",
        cascade="all, delete-orphan"
    )

    gaze_payload_archives: Mapped[list["GazePayloadArchive"]] = relationship(
        "GazePayloadArchive",
        back_populates="study_session",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<StudySession(study_session_id={self.study_session_id}, "
            f"participant_id={self.participant_id}, survey_id={self.survey_id})>"
        )


class ParticipantInteractionLog(Base):
    __tablename__ = "participant_interaction_logs"

    interaction_log_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )

    study_session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("study_sessions.study_session_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    post_id: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True
    )

    view_mode: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    event_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        index=True
    )

    event_payload: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    study_session: Mapped["StudySession"] = relationship(
        "StudySession",
        back_populates="interaction_logs"
    )

    def __repr__(self) -> str:
        return (
            f"<ParticipantInteractionLog(interaction_log_id={self.interaction_log_id}, "
            f"event_type={self.event_type}, post_id={self.post_id})>"
        )