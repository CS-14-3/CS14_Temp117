from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project_database.db import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Survey(Base):
    __tablename__ = "surveys"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )
    researcher_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("researchers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="draft"
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

    researcher: Mapped["Researcher"] = relationship(
        "Researcher",
        back_populates="surveys"
    )
    news_items: Mapped[list["SurveyNewsItem"]] = relationship(
        "SurveyNewsItem",
        back_populates="survey",
        cascade="all, delete-orphan",
        order_by="SurveyNewsItem.sort_order"
    )
    publications: Mapped[list["SurveyPublication"]] = relationship(
        "SurveyPublication",
        back_populates="survey",
        cascade="all, delete-orphan",
        order_by="SurveyPublication.published_at"
    )

    def __repr__(self) -> str:
        return f"<Survey(id={self.id}, researcher_id={self.researcher_id}, status={self.status})>"


class SurveyNewsItem(Base):
    __tablename__ = "survey_news_items"
    __table_args__ = (
        UniqueConstraint("survey_id", "sort_order", name="uq_survey_news_items_order"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )
    survey_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("surveys.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    source_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    scraped_title: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    survey: Mapped["Survey"] = relationship(
        "Survey",
        back_populates="news_items"
    )
    variants: Mapped[list["SurveyVariant"]] = relationship(
        "SurveyVariant",
        back_populates="news_item",
        cascade="all, delete-orphan"
    )
    participant_answers: Mapped[list["ParticipantAnswer"]] = relationship(
        "ParticipantAnswer",
        back_populates="news_item"
    )

    def __repr__(self) -> str:
        return f"<SurveyNewsItem(id={self.id}, survey_id={self.survey_id}, sort_order={self.sort_order})>"


class SurveyVariant(Base):
    __tablename__ = "survey_variants"
    __table_args__ = (
        UniqueConstraint("news_item_id", "version_key", "platform", name="uq_survey_variants_identity"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )
    news_item_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("survey_news_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    version_key: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )
    platform: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    caption: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    avatar_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    handle: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    hidden_elements_json: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )
    question_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    question_required: Mapped[bool] = mapped_column(
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

    news_item: Mapped["SurveyNewsItem"] = relationship(
        "SurveyNewsItem",
        back_populates="variants"
    )
    question_options: Mapped[list["SurveyQuestionOption"]] = relationship(
        "SurveyQuestionOption",
        back_populates="variant",
        cascade="all, delete-orphan",
        order_by="SurveyQuestionOption.sort_order"
    )
    participant_answers: Mapped[list["ParticipantAnswer"]] = relationship(
        "ParticipantAnswer",
        back_populates="variant"
    )

    def __repr__(self) -> str:
        return (
            f"<SurveyVariant(id={self.id}, news_item_id={self.news_item_id}, "
            f"version_key={self.version_key}, platform={self.platform})>"
        )


class SurveyQuestionOption(Base):
    __tablename__ = "survey_question_options"
    __table_args__ = (
        UniqueConstraint("variant_id", "sort_order", name="uq_survey_question_options_order"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )
    variant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("survey_variants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    option_label: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    variant: Mapped["SurveyVariant"] = relationship(
        "SurveyVariant",
        back_populates="question_options"
    )
    participant_answers: Mapped[list["ParticipantAnswer"]] = relationship(
        "ParticipantAnswer",
        back_populates="option"
    )

    def __repr__(self) -> str:
        return f"<SurveyQuestionOption(id={self.id}, variant_id={self.variant_id}, sort_order={self.sort_order})>"


class SurveyPublication(Base):
    __tablename__ = "survey_publications"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )
    survey_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("surveys.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    invite_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
        index=True
    )
    published_version_key: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )
    published_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    survey: Mapped["Survey"] = relationship(
        "Survey",
        back_populates="publications"
    )
    participant_sessions: Mapped[list["ParticipantSession"]] = relationship(
        "ParticipantSession",
        back_populates="publication",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<SurveyPublication(id={self.id}, survey_id={self.survey_id}, invite_code={self.invite_code})>"
