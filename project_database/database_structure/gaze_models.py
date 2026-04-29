from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project_database.db import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CalibrationResult(Base):
    __tablename__ = "calibration_results"

    calibration_result_id: Mapped[str] = mapped_column(
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

    overall_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    score_percent: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    passed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    quality_threshold: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    total_points: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    raw_quality_metrics: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    study_session: Mapped["StudySession"] = relationship(
        "StudySession",
        back_populates="calibration_results"
    )

    calibration_samples: Mapped[list["CalibrationSample"]] = relationship(
        "CalibrationSample",
        back_populates="calibration_result",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<CalibrationResult(calibration_result_id={self.calibration_result_id}, "
            f"study_session_id={self.study_session_id}, passed={self.passed})>"
        )


class CalibrationSample(Base):
    __tablename__ = "calibration_samples"

    calibration_sample_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )

    calibration_result_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("calibration_results.calibration_result_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    study_session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("study_sessions.study_session_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    target_index: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    target_x: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )
    target_y: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    iris_x: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )
    iris_y: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    sample_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        index=True
    )

    calibration_result: Mapped["CalibrationResult"] = relationship(
        "CalibrationResult",
        back_populates="calibration_samples"
    )

    study_session = relationship("StudySession")

    def __repr__(self) -> str:
        return (
            f"<CalibrationSample(calibration_sample_id={self.calibration_sample_id}, "
            f"target_index={self.target_index})>"
        )


class GazeRecord(Base):
    __tablename__ = "gaze_records"

    gaze_record_id: Mapped[str] = mapped_column(
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

    survey_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("surveys.survey_id", ondelete="SET NULL"),
        nullable=True,
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

    iris_x: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )
    iris_y: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )
    iris_z: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    face_detected: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    gaze_region: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True
    )

    screen_x: Mapped[float | None] = mapped_column(Float, nullable=True)
    screen_y: Mapped[float | None] = mapped_column(Float, nullable=True)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        index=True
    )

    study_session: Mapped["StudySession"] = relationship(
        "StudySession",
        back_populates="gaze_records"
    )

    survey = relationship("Survey")

    def __repr__(self) -> str:
        return (
            f"<GazeRecord(gaze_record_id={self.gaze_record_id}, "
            f"study_session_id={self.study_session_id}, post_id={self.post_id})>"
        )


class GazePayloadArchive(Base):
    __tablename__ = "gaze_payload_archives"

    payload_archive_id: Mapped[str] = mapped_column(
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

    payload_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )

    payload_json: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    saved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        index=True
    )

    study_session: Mapped["StudySession"] = relationship(
        "StudySession",
        back_populates="gaze_payload_archives"
    )

    def __repr__(self) -> str:
        return (
            f"<GazePayloadArchive(payload_archive_id={self.payload_archive_id}, "
            f"payload_type={self.payload_type})>"
        )