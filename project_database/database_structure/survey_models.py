from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project_database.db import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Survey(Base):
    __tablename__ = "surveys"

    survey_id: Mapped[str] = mapped_column(
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

    # Basic project / survey info
    survey_title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    research_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # News link scraping source
    news_link: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    scraped_title: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    scraped_image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # Access / publishing state
    invite_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        index=True
    )
    survey_link: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft"
    )
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
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

    # Relationships
    versions: Mapped[list["SurveyVersion"]] = relationship(
        "SurveyVersion",
        back_populates="survey",
        cascade="all, delete-orphan"
    )

    publish_logs: Mapped[list["SurveyPublishLog"]] = relationship(
        "SurveyPublishLog",
        back_populates="survey",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Survey(survey_id={self.survey_id}, researcher_id={self.researcher_id}, status={self.status})>"


class SurveyVersion(Base):
    __tablename__ = "survey_versions"

    survey_version_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )

    survey_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("surveys.survey_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # A/B version identity
    version_label: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    # Editable researcher-main fields
    platform: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="instagram"
    )
    caption: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    likes_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    comments_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    shares_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
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

    survey: Mapped["Survey"] = relationship(
        "Survey",
        back_populates="versions"
    )

    publish_logs: Mapped[list["SurveyPublishLog"]] = relationship(
        "SurveyPublishLog",
        back_populates="survey_version"
    )

    def __repr__(self) -> str:
        return (
            f"<SurveyVersion(survey_version_id={self.survey_version_id}, "
            f"survey_id={self.survey_id}, version_label={self.version_label})>"
        )


class SurveyPublishLog(Base):
    __tablename__ = "survey_publish_logs"

    publish_log_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )

    survey_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("surveys.survey_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    survey_version_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("survey_versions.survey_version_id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    published_by_researcher_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("researchers.researcher_id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    invite_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True
    )
    participant_link: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # Snapshot of what was actually published
    version_label: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )
    platform: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="instagram"
    )
    caption: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    likes_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    comments_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    shares_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    published_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    survey: Mapped["Survey"] = relationship(
        "Survey",
        back_populates="publish_logs"
    )

    survey_version: Mapped["SurveyVersion | None"] = relationship(
        "SurveyVersion",
        back_populates="publish_logs"
    )

    def __repr__(self) -> str:
        return (
            f"<SurveyPublishLog(publish_log_id={self.publish_log_id}, "
            f"survey_id={self.survey_id}, invite_code={self.invite_code})>"
        )