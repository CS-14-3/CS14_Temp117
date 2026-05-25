from __future__ import annotations

import csv
import io
import json
import secrets
import string
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session, joinedload

from project_database.db import SessionLocal, init_db
from project_database.database_structure.auth_models import Researcher
from project_database.database_structure.participant_models import ParticipantAnswer, ParticipantSession
from project_database.database_structure.survey_models import (
    Survey,
    SurveyNewsItem,
    SurveyPublication,
    SurveyQuestionOption,
    SurveyVariant,
)


DEFAULT_USERNAME = "sydney_news_hub"
DEFAULT_HANDLE = "@sydneynews"
DEFAULT_LOCATION = "Sydney, Australia"
DEFAULT_TIME_LABEL = "Just now"
MIN_AWARE_DATETIME = datetime.min.replace(tzinfo=timezone.utc)
PRESENTATION_ICONS_KEY = "_presentationIcons"
PRESENTATION_ACTION_BUTTONS_KEY = "_presentationActionButtons"
PRESENTATION_INTERNAL_KEYS = {
    PRESENTATION_ICONS_KEY,
    PRESENTATION_ACTION_BUTTONS_KEY,
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_email(value: Any) -> str:
    return str(value or "").strip().lower()


def normalize_invite_code(value: Any) -> str:
    allowed = string.ascii_uppercase + string.digits
    raw = str(value or "").upper()
    cleaned = "".join(ch for ch in raw if ch in allowed)
    return cleaned[:20]


def safe_json_clone(value: Any) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


def iso_to_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


@contextmanager
def get_session() -> Session:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


class DBBridge:
    def __init__(self, auto_init: bool = False) -> None:
        if auto_init:
            init_db()

    # ------------------------------------------------------------------
    # Researcher auth
    # ------------------------------------------------------------------
    def register_researcher(
        self,
        *,
        name: str | None,
        email: str,
        password: str,
        role: str = "researcher",
    ) -> dict[str, Any]:
        del role
        username = normalize_email(email)
        password = str(password or "").strip()
        display_name = str(name or "").strip() or username.split("@", 1)[0] or "Researcher"

        if not username:
            raise ValueError("Email is required.")
        if not password:
            raise ValueError("Password is required.")

        with get_session() as db:
            existing = db.query(Researcher).filter(Researcher.username == username).one_or_none()
            if existing is not None:
                raise ValueError("This email is already registered.")

            researcher = Researcher(username=username, password_hash=password)
            db.add(researcher)
            db.flush()

            return {
                "researcher_id": researcher.id,
                "email": researcher.username,
                "name": display_name,
                "initial": (display_name[:1] or "R").upper(),
                "session_token": secrets.token_urlsafe(24),
                "session_id": researcher.id,
            }

    def login_researcher(
        self,
        *,
        email: str,
        password: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> dict[str, Any] | None:
        del ip_address, user_agent
        username = normalize_email(email)
        password = str(password or "").strip()

        with get_session() as db:
            researcher = db.query(Researcher).filter(Researcher.username == username).one_or_none()
            if researcher is None or researcher.password_hash != password:
                return None

            display_name = username.split("@", 1)[0] or username or "Researcher"
            return {
                "researcher_id": researcher.id,
                "email": researcher.username,
                "name": display_name,
                "initial": (display_name[:1] or "R").upper(),
                "session_token": secrets.token_urlsafe(24),
                "session_id": researcher.id,
            }

    def get_researcher_by_session_token(self, session_token: str) -> dict[str, Any] | None:
        del session_token
        return None

    def revoke_session(self, session_token: str) -> bool:
        del session_token
        return False

    def get_researcher_by_email(self, email: str) -> dict[str, Any] | None:
        username = normalize_email(email)
        if not username:
            return None

        with get_session() as db:
            researcher = db.query(Researcher).filter(Researcher.username == username).one_or_none()
            if researcher is None:
                return None
            return self._researcher_to_dict(researcher)

    # ------------------------------------------------------------------
    # Survey publishing
    # ------------------------------------------------------------------
    def publish_survey_snapshot(self, *, researcher_email: str, snapshot: dict[str, Any]) -> dict[str, Any]:
        researcher = self.get_researcher_by_email(researcher_email)
        if researcher is None:
            raise ValueError("Researcher account not found.")

        invite_code = normalize_invite_code(snapshot.get("inviteCode"))
        if not invite_code:
            raise ValueError("Invite code is required before publishing.")

        title = str(snapshot.get("title") or "Untitled survey").strip() or "Untitled survey"
        published_version_key = str(snapshot.get("publishedVersionKey") or "vA").strip() or "vA"
        published_at = iso_to_datetime(snapshot.get("publishedAt")) or utc_now()
        news_payloads = snapshot.get("news") if isinstance(snapshot.get("news"), list) else []
        if not news_payloads:
            raise ValueError("At least one news item is required before publishing.")

        with get_session() as db:
            existing_publication = (
                db.query(SurveyPublication)
                .filter(SurveyPublication.invite_code == invite_code)
                .one_or_none()
            )
            if existing_publication is not None:
                raise ValueError("This invite code is already in use.")

            survey = Survey(
                researcher_id=researcher["researcher_id"],
                title=title,
                status="published",
                created_at=iso_to_datetime(snapshot.get("createdAt")) or published_at,
                updated_at=published_at,
            )
            db.add(survey)
            db.flush()

            saved_posts: list[dict[str, Any]] = []
            for index, news_payload in enumerate(news_payloads, start=1):
                news_item = SurveyNewsItem(
                    survey_id=survey.id,
                    sort_order=index,
                    source_url=str(news_payload.get("link") or "").strip(),
                    scraped_title=self._extract_news_title(news_payload),
                    created_at=published_at,
                )
                db.add(news_item)
                db.flush()

                version_key = str(news_payload.get("publishedVersionKey") or published_version_key).strip() or published_version_key
                variant_payload = self._extract_published_variant(news_payload, version_key)
                question_block = self._normalize_question_block(variant_payload.get("questionBlock"))
                hidden_elements = dict(self._normalize_hidden_elements(variant_payload.get("hiddenElements")) or {})
                for internal_key in PRESENTATION_INTERNAL_KEYS:
                    hidden_elements.pop(internal_key, None)
                icons = variant_payload.get("icons")
                action_buttons = variant_payload.get("actionButtons")
                if isinstance(icons, dict):
                    hidden_elements[PRESENTATION_ICONS_KEY] = safe_json_clone(icons)
                if isinstance(action_buttons, list):
                    hidden_elements[PRESENTATION_ACTION_BUTTONS_KEY] = safe_json_clone(action_buttons)
                if question_block.get("type") == "multiple":
                    hidden_elements = {**hidden_elements, "_questionBlockType": "multiple"}
                else:
                    hidden_elements.pop("_questionBlockType", None)
                variant = SurveyVariant(
                    news_item_id=news_item.id,
                    version_key=version_key,
                    platform=self._normalize_platform(variant_payload.get("platform")),
                    caption=str(variant_payload.get("caption") or "").strip() or None,
                    image_url=self._empty_to_none(variant_payload.get("image")),
                    avatar_url=self._empty_to_none(variant_payload.get("avatar")),
                    username=self._empty_to_none(variant_payload.get("username")),
                    handle=self._empty_to_none(variant_payload.get("handle")),
                    hidden_elements_json=hidden_elements or None,
                    question_text=self._empty_to_none(question_block.get("questionText")),
                    question_required=bool(question_block.get("required")),
                    created_at=published_at,
                    updated_at=published_at,
                )
                db.add(variant)
                db.flush()

                for option_index, option in enumerate(question_block.get("options", []), start=1):
                    option_obj = SurveyQuestionOption(
                        variant_id=variant.id,
                        sort_order=option_index,
                        option_label=str(option.get("label") or f"Option {option_index}").strip() or f"Option {option_index}",
                    )
                    db.add(option_obj)
                    db.flush()

                saved_posts.append(self._build_participant_post(db, news_item, variant, invite_code, index))

            publication = SurveyPublication(
                survey_id=survey.id,
                invite_code=invite_code,
                published_version_key=published_version_key,
                published_at=published_at,
            )
            db.add(publication)
            db.flush()

            return {
                "survey": self._survey_to_dict(survey),
                "publication": self._publication_to_dict(publication),
                "posts": saved_posts,
            }

    def create_survey(
        self,
        *,
        researcher_id: str,
        news_link: str | None = None,
        scraped_title: str | None = None,
        scraped_image_url: str | None = None,
    ) -> dict[str, Any]:
        del scraped_image_url
        title = str(scraped_title or "Untitled survey").strip() or "Untitled survey"
        with get_session() as db:
            survey = Survey(researcher_id=researcher_id, title=title, status="draft")
            db.add(survey)
            db.flush()
            if news_link:
                news_item = SurveyNewsItem(
                    survey_id=survey.id,
                    sort_order=1,
                    source_url=str(news_link).strip(),
                    scraped_title=scraped_title,
                )
                db.add(news_item)
                db.flush()
            return self._survey_to_dict(survey)

    def upsert_survey_version(
        self,
        *,
        survey_id: str,
        version_label: str,
        platform: str,
        caption: str | None = None,
        image_url: str | None = None,
        likes_count: int | None = None,
        comments_count: int | None = None,
        shares_count: int | None = None,
        is_default: bool = False,
    ) -> dict[str, Any]:
        del likes_count, comments_count, shares_count, is_default
        with get_session() as db:
            news_item = (
                db.query(SurveyNewsItem)
                .filter(SurveyNewsItem.survey_id == survey_id)
                .order_by(SurveyNewsItem.sort_order.asc())
                .first()
            )
            if news_item is None:
                news_item = SurveyNewsItem(survey_id=survey_id, sort_order=1, source_url="", scraped_title=None)
                db.add(news_item)
                db.flush()

            variant = (
                db.query(SurveyVariant)
                .filter(
                    SurveyVariant.news_item_id == news_item.id,
                    SurveyVariant.version_key == version_label,
                    SurveyVariant.platform == self._normalize_platform(platform),
                )
                .one_or_none()
            )
            if variant is None:
                variant = SurveyVariant(
                    news_item_id=news_item.id,
                    version_key=version_label,
                    platform=self._normalize_platform(platform),
                )
                db.add(variant)

            variant.caption = self._empty_to_none(caption)
            variant.image_url = self._empty_to_none(image_url)
            db.flush()
            return self._variant_to_legacy_dict(variant)

    def publish_survey_version(
        self,
        *,
        survey_id: str,
        version_label: str,
        published_by_researcher_id: str | None = None,
        invite_code: str | None = None,
        participant_link: str | None = None,
    ) -> dict[str, Any]:
        del published_by_researcher_id, participant_link
        with get_session() as db:
            survey = db.query(Survey).filter(Survey.id == survey_id).one()
            invite = normalize_invite_code(invite_code) or self._generate_unique_invite_code(db)
            existing = db.query(SurveyPublication).filter(SurveyPublication.invite_code == invite).one_or_none()
            if existing is not None:
                raise ValueError("This invite code is already in use.")
            publication = SurveyPublication(
                survey_id=survey.id,
                invite_code=invite,
                published_version_key=version_label,
            )
            survey.status = "published"
            db.add(publication)
            db.flush()
            return {
                "survey": self._survey_to_dict(survey),
                "publish_log": self._publication_to_legacy_dict(publication, db),
            }

    def get_published_posts_by_invite_code(self, invite_code: str) -> list[dict[str, Any]]:
        code = normalize_invite_code(invite_code)
        if not code:
            return []

        with get_session() as db:
            publication = (
                db.query(SurveyPublication)
                .options(
                    joinedload(SurveyPublication.survey)
                    .joinedload(Survey.news_items)
                    .joinedload(SurveyNewsItem.variants)
                    .joinedload(SurveyVariant.question_options)
                )
                .filter(SurveyPublication.invite_code == code)
                .order_by(SurveyPublication.published_at.desc())
                .first()
            )
            if publication is None or publication.survey is None:
                return []

            posts: list[dict[str, Any]] = []
            for index, news_item in enumerate(sorted(publication.survey.news_items, key=lambda item: item.sort_order), start=1):
                variant = self._pick_variant_for_publication(news_item, publication.published_version_key)
                if variant is None:
                    continue
                posts.append(self._build_participant_post(db, news_item, variant, publication.invite_code, index))
            return posts

    def generate_unique_invite_code(self, length: int = 6) -> str:
        with get_session() as db:
            return self._generate_unique_invite_code(db, length=length)

    def get_survey_id_by_invite_code(self, invite_code: str) -> str | None:
        code = normalize_invite_code(invite_code)
        if not code:
            return None

        with get_session() as db:
            publication = (
                db.query(SurveyPublication)
                .filter(SurveyPublication.invite_code == code)
                .order_by(SurveyPublication.published_at.desc())
                .first()
            )
            return publication.survey_id if publication is not None else None

    def list_study_sessions_for_researcher(self, researcher_email: str) -> list[dict[str, Any]]:
        researcher = self.get_researcher_by_email(researcher_email)
        if researcher is None:
            return []

        with get_session() as db:
            sessions = (
                db.query(ParticipantSession)
                .join(ParticipantSession.publication)
                .join(SurveyPublication.survey)
                .options(joinedload(ParticipantSession.publication))
                .filter(
                    Survey.researcher_id == researcher["researcher_id"],
                    ParticipantSession.closed_at.isnot(None),
                )
                .order_by(ParticipantSession.closed_at.desc().nullslast(), ParticipantSession.started_at.desc().nullslast())
                .all()
            )

            return [self._study_session_summary(session) for session in sessions]

    def get_study_session_payload_for_researcher(self, researcher_email: str, filename: str) -> dict[str, Any] | None:
        researcher = self.get_researcher_by_email(researcher_email)
        if researcher is None:
            return None

        session_id = self._study_session_id_from_filename(filename)
        if not session_id:
            return None

        with get_session() as db:
            session = (
                db.query(ParticipantSession)
                .join(ParticipantSession.publication)
                .join(SurveyPublication.survey)
                .filter(
                    ParticipantSession.id == session_id,
                    Survey.researcher_id == researcher["researcher_id"],
                )
                .one_or_none()
            )
            if session is None:
                return None

            payload = safe_json_clone(session.gaze_data_json or {})
            if isinstance(payload, dict):
                payload.setdefault("participantId", self._session_participant_id(session))
                payload.setdefault("inviteCode", session.publication.invite_code if session.publication else "")
                payload.setdefault("studySessionId", session.id)
                payload.setdefault("startedAt", session.started_at.isoformat() if session.started_at else "")
                payload.setdefault("closedAt", session.closed_at.isoformat() if session.closed_at else "")
                if "gazeLogs" not in payload and isinstance(payload.get("gazeData"), list):
                    payload["gazeLogs"] = payload["gazeData"]
                if "posts" not in payload and session.publication is not None:
                    payload["posts"] = self._study_session_posts(session.publication)
            return payload

    def export_survey_non_gaze_csv_for_researcher(self, researcher_email: str, survey_id_or_invite_code: str) -> str | None:
        researcher = self.get_researcher_by_email(researcher_email)
        if researcher is None:
            return None

        with get_session() as db:
            query = (
                db.query(Survey)
                .options(
                    joinedload(Survey.news_items)
                    .joinedload(SurveyNewsItem.variants)
                    .joinedload(SurveyVariant.question_options),
                    joinedload(Survey.publications)
                    .joinedload(SurveyPublication.participant_sessions)
                    .joinedload(ParticipantSession.answers),
                )
            )
            survey = (
                query
                .filter(
                    Survey.id == survey_id_or_invite_code,
                    Survey.researcher_id == researcher["researcher_id"],
                )
                .one_or_none()
            )
            if survey is None:
                survey = (
                    query
                    .join(Survey.publications)
                    .filter(
                        SurveyPublication.invite_code == normalize_invite_code(survey_id_or_invite_code),
                        Survey.researcher_id == researcher["researcher_id"],
                    )
                    .one_or_none()
                )
            if survey is None:
                return None

            rows = self._survey_non_gaze_export_rows(survey)

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self._survey_non_gaze_export_columns())
        writer.writeheader()
        writer.writerows(rows)
        return output.getvalue()

    # ------------------------------------------------------------------
    # Participant sessions / payload archival
    # ------------------------------------------------------------------
    def upsert_full_study_payload(
        self,
        *,
        participant_code: str,
        survey_id: str | None,
        invite_code: str | None,
        payload_type: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        del participant_code, payload_type
        normalized_invite = normalize_invite_code(invite_code)
        started_at = (
            iso_to_datetime(payload.get("startedAt"))
            or iso_to_datetime(payload.get("studyStartedAt"))
            or utc_now()
        )
        closed_at = iso_to_datetime(payload.get("closedAt")) or iso_to_datetime(payload.get("studyEndedAt"))
        status = "completed" if closed_at else "started"
        gaze_logs = payload.get("gazeLogs") if isinstance(payload.get("gazeLogs"), list) else []

        with get_session() as db:
            publication = None
            if normalized_invite:
                publication = (
                    db.query(SurveyPublication)
                    .filter(SurveyPublication.invite_code == normalized_invite)
                    .order_by(SurveyPublication.published_at.desc())
                    .first()
                )
            if publication is None and survey_id:
                publication = (
                    db.query(SurveyPublication)
                    .filter(SurveyPublication.survey_id == survey_id)
                    .order_by(SurveyPublication.published_at.desc())
                    .first()
                )
            if publication is None:
                raise ValueError("No published survey matches this payload.")

            session = (
                db.query(ParticipantSession)
                .filter(
                    ParticipantSession.publication_id == publication.id,
                    ParticipantSession.started_at == started_at,
                )
                .one_or_none()
            )
            if session is None:
                session = ParticipantSession(
                    publication_id=publication.id,
                    started_at=started_at,
                    closed_at=closed_at,
                    status=status,
                    gaze_data_json=safe_json_clone(payload),
                )
                db.add(session)
                db.flush()
            else:
                session.closed_at = closed_at or session.closed_at
                session.status = status if status == "completed" else session.status
                session.gaze_data_json = safe_json_clone(payload)
                db.flush()

            self._upsert_answers_from_payload(db, session, publication, payload)

            return {
                "study_session_id": session.id,
                "gaze_records_saved": len(gaze_logs),
                "calibration_samples_saved": len(payload.get("calibrationLogs", []) or []),
                "interaction_logs_saved": 0,
            }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _study_session_filename(self, session: ParticipantSession) -> str:
        return f"CS14_DB_{session.id}.json"

    def _study_session_id_from_filename(self, filename: str) -> str | None:
        text = str(filename or "").strip()
        if not text.startswith("CS14_DB_") or not text.endswith(".json"):
            return None
        session_id = text[len("CS14_DB_"):-len(".json")]
        return session_id if session_id else None

    def _session_participant_id(self, session: ParticipantSession) -> str:
        payload = session.gaze_data_json if isinstance(session.gaze_data_json, dict) else {}
        participant_id = (
            payload.get("participantId")
            or payload.get("participant_id")
            or payload.get("participantCode")
            or payload.get("participant_code")
        )
        if participant_id:
            return str(participant_id)
        if session.publication is not None and session.publication.invite_code:
            return session.publication.invite_code
        return session.id[:6].upper()

    def _study_session_summary(self, session: ParticipantSession) -> dict[str, Any]:
        payload = session.gaze_data_json if isinstance(session.gaze_data_json, dict) else {}
        closed_at = session.closed_at or iso_to_datetime(payload.get("closedAt")) or iso_to_datetime(payload.get("studyEndedAt"))
        started_at = session.started_at or iso_to_datetime(payload.get("startedAt")) or iso_to_datetime(payload.get("studyStartedAt"))
        display_time = closed_at or started_at
        encoded_payload = json.dumps(payload or {}, ensure_ascii=False, default=str).encode("utf-8")
        sample_count = 0
        gaze_logs = payload.get("gazeLogs") or payload.get("gazeData") if isinstance(payload, dict) else []
        if isinstance(gaze_logs, list):
            sample_count = len(gaze_logs)

        return {
            "filename": self._study_session_filename(session),
            "sessionId": session.id,
            "participantId": self._session_participant_id(session),
            "inviteCode": session.publication.invite_code if session.publication is not None else "",
            "status": session.status,
            "startedAt": started_at.isoformat() if started_at else "",
            "completedAt": closed_at.isoformat() if closed_at else "",
            "dateLabel": display_time.isoformat() if display_time else "",
            "fileSizeKb": round(len(encoded_payload) / 1024),
            "sampleCount": sample_count,
        }

    def _study_session_posts(self, publication: SurveyPublication) -> list[dict[str, Any]]:
        posts = []
        survey = publication.survey
        if survey is None:
            return posts
        for index, news_item in enumerate(sorted(survey.news_items, key=lambda item: item.sort_order), start=1):
            variant = self._pick_variant_for_publication(news_item, publication.published_version_key)
            if variant is None:
                continue
            posts.append({
                "index": index,
                "id": f"{publication.invite_code}_{index}",
                "platform": variant.platform,
                "username": variant.username or DEFAULT_USERNAME,
            })
        return posts

    def _survey_non_gaze_export_columns(self) -> list[str]:
        return [
            "surveys.id",
            "surveys.title",
            "surveys.status",
            "survey_news_items.id",
            "survey_news_items.sort_order",
            "survey_news_items.source_url",
            "survey_news_items.scraped_title",
            "survey_variants.id",
            "survey_variants.version_key",
            "survey_variants.platform",
            "survey_variants.caption",
            "survey_variants.image_url",
            "survey_variants.avatar_url",
            "survey_variants.username",
            "survey_variants.handle",
            "survey_variants.question_text",
            "survey_variants.question_required",
            "survey_question_options.id",
            "survey_question_options.sort_order",
            "survey_question_options.option_label",
            "survey_publications.id",
            "survey_publications.invite_code",
            "survey_publications.published_version_key",
            "survey_publications.published_at",
            "participant_sessions.id",
            "participant_sessions.status",
            "participant_sessions.started_at",
            "participant_sessions.closed_at",
            "participant_answers.id",
            "participant_answers.session_id",
            "participant_answers.news_item_id",
            "participant_answers.variant_id",
            "participant_answers.option_id",
            "participant_answers.answered_at",
        ]

    def _survey_non_gaze_export_rows(self, survey: Survey) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        publications = sorted(survey.publications, key=lambda publication: publication.published_at or MIN_AWARE_DATETIME)
        if not publications:
            publications = [None]

        for news_item in sorted(survey.news_items, key=lambda item: item.sort_order):
            variants = sorted(news_item.variants, key=lambda variant: (variant.version_key, variant.platform))
            if not variants:
                variants = [None]

            for variant in variants:
                options = sorted(variant.question_options, key=lambda option: option.sort_order) if variant else []
                if not options:
                    options = [None]

                for option in options:
                    row_added = False
                    for publication in publications:
                        sessions = sorted(
                            publication.participant_sessions,
                            key=lambda item: item.started_at or MIN_AWARE_DATETIME,
                        ) if publication else []
                        if not sessions:
                            rows.append(self._survey_non_gaze_export_row(
                                survey=survey,
                                news_item=news_item,
                                variant=variant,
                                option=option,
                                publication=publication,
                                session=None,
                                answer=None,
                            ))
                            row_added = True
                            continue

                        for session in sessions:
                            answers = [
                                answer for answer in session.answers
                                if answer.news_item_id == news_item.id
                                and (variant is None or answer.variant_id == variant.id)
                                and (option is None or answer.option_id == option.id)
                            ]
                            if answers:
                                for answer in answers:
                                    rows.append(self._survey_non_gaze_export_row(
                                        survey=survey,
                                        news_item=news_item,
                                        variant=variant,
                                        option=option,
                                        publication=publication,
                                        session=session,
                                        answer=answer,
                                    ))
                                    row_added = True
                            else:
                                rows.append(self._survey_non_gaze_export_row(
                                    survey=survey,
                                    news_item=news_item,
                                    variant=variant,
                                    option=option,
                                    publication=publication,
                                    session=session,
                                    answer=None,
                                ))
                                row_added = True

                    if not row_added:
                        rows.append(self._survey_non_gaze_export_row(
                            survey=survey,
                            news_item=news_item,
                            variant=variant,
                            option=option,
                            publication=None,
                            session=None,
                            answer=None,
                        ))
        return rows

    def _survey_non_gaze_export_row(
        self,
        *,
        survey: Survey,
        news_item: SurveyNewsItem,
        variant: SurveyVariant | None,
        option: SurveyQuestionOption | None,
        publication: SurveyPublication | None,
        session: ParticipantSession | None,
        answer: ParticipantAnswer | None,
    ) -> dict[str, Any]:
        return {
            "surveys.id": survey.id,
            "surveys.title": survey.title,
            "surveys.status": survey.status,
            "survey_news_items.id": news_item.id,
            "survey_news_items.sort_order": news_item.sort_order,
            "survey_news_items.source_url": news_item.source_url,
            "survey_news_items.scraped_title": news_item.scraped_title,
            "survey_variants.id": variant.id if variant else "",
            "survey_variants.version_key": variant.version_key if variant else "",
            "survey_variants.platform": variant.platform if variant else "",
            "survey_variants.caption": variant.caption if variant else "",
            "survey_variants.image_url": variant.image_url if variant else "",
            "survey_variants.avatar_url": variant.avatar_url if variant else "",
            "survey_variants.username": variant.username if variant else "",
            "survey_variants.handle": variant.handle if variant else "",
            "survey_variants.question_text": variant.question_text if variant else "",
            "survey_variants.question_required": variant.question_required if variant else "",
            "survey_question_options.id": option.id if option else "",
            "survey_question_options.sort_order": option.sort_order if option else "",
            "survey_question_options.option_label": option.option_label if option else "",
            "survey_publications.id": publication.id if publication else "",
            "survey_publications.invite_code": publication.invite_code if publication else "",
            "survey_publications.published_version_key": publication.published_version_key if publication else "",
            "survey_publications.published_at": publication.published_at.isoformat() if publication and publication.published_at else "",
            "participant_sessions.id": session.id if session else "",
            "participant_sessions.status": session.status if session else "",
            "participant_sessions.started_at": session.started_at.isoformat() if session and session.started_at else "",
            "participant_sessions.closed_at": session.closed_at.isoformat() if session and session.closed_at else "",
            "participant_answers.id": answer.id if answer else "",
            "participant_answers.session_id": answer.session_id if answer else "",
            "participant_answers.news_item_id": answer.news_item_id if answer else "",
            "participant_answers.variant_id": answer.variant_id if answer else "",
            "participant_answers.option_id": answer.option_id if answer else "",
            "participant_answers.answered_at": answer.answered_at.isoformat() if answer and answer.answered_at else "",
        }

    def _pick_variant_for_publication(self, news_item: SurveyNewsItem, published_version_key: str) -> SurveyVariant | None:
        exact = [variant for variant in news_item.variants if variant.version_key == published_version_key]
        if exact:
            return exact[0]
        return news_item.variants[0] if news_item.variants else None

    def _build_participant_post(
        self,
        db: Session,
        news_item: SurveyNewsItem,
        variant: SurveyVariant,
        invite_code: str,
        index: int,
    ) -> dict[str, Any]:
        del db
        hidden = variant.hidden_elements_json or {}
        icons = hidden.get(PRESENTATION_ICONS_KEY)
        action_buttons = hidden.get(PRESENTATION_ACTION_BUTTONS_KEY)
        has_configured_action_buttons = isinstance(action_buttons, list)
        hidden_for_client = {
            key: value
            for key, value in hidden.items()
            if key != "_questionBlockType" and key not in PRESENTATION_INTERNAL_KEYS
        }
        username = variant.username or DEFAULT_USERNAME
        handle = variant.handle or DEFAULT_HANDLE
        options = [
            {"id": option.id, "label": option.option_label}
            for option in sorted(variant.question_options, key=lambda item: item.sort_order)
        ]
        question_enabled = bool((variant.question_text or "").strip() and options)
        question_type = "multiple" if hidden.get("_questionBlockType") == "multiple" else "single"
        return {
            "id": f"{invite_code}_{index}",
            "inviteCode": invite_code,
            "surveyId": news_item.survey_id,
            "newsIndex": index,
            "newsLink": news_item.source_url,
            "versionKey": variant.version_key,
            "platform": variant.platform,
            "caption": variant.caption or "",
            "image": "" if hidden.get("image") else (variant.image_url or ""),
            "avatar": "" if hidden.get("avatar") else (variant.avatar_url or ""),
            "likes": 0,
            "comments": 0,
            "shares": 0,
            "username": "" if hidden.get("username") else username,
            "handle": handle,
            "location": "",
            "time": DEFAULT_TIME_LABEL,
            "hiddenElements": hidden_for_client,
            "icons": icons if isinstance(icons, dict) else {},
            "actionButtons": action_buttons if has_configured_action_buttons else [],
            "actionButtonsConfigured": has_configured_action_buttons,
            "questionBlock": {
                "enabled": question_enabled,
                "type": question_type,
                "questionText": variant.question_text or "",
                "required": bool(variant.question_required),
                "options": options,
            },
        }

    def _normalize_platform(self, value: Any) -> str:
        platform = str(value or "instagram").strip().lower()
        if platform in {"twitter", "x"}:
            return "x"
        if platform in {"instagram", "facebook", "tiktok"}:
            return platform
        return "instagram"

    def _empty_to_none(self, value: Any) -> str | None:
        text = str(value or "").strip()
        return text or None

    def _extract_news_title(self, news_payload: dict[str, Any]) -> str | None:
        title = str(news_payload.get("title") or news_payload.get("scraped_title") or "").strip()
        if title:
            return title
        variant = self._extract_published_variant(news_payload, str(news_payload.get("publishedVersionKey") or "vA"))
        return self._empty_to_none(variant.get("caption"))

    def _extract_published_variant(self, news_payload: dict[str, Any], version_key: str) -> dict[str, Any]:
        versions = news_payload.get("versions") if isinstance(news_payload.get("versions"), dict) else {}
        version_payload = versions.get(version_key) or next(iter(versions.values()), {})
        if not isinstance(version_payload, dict):
            version_payload = {}
        platform = self._normalize_platform(version_payload.get("platform"))
        platform_variants = version_payload.get("platformVariants") if isinstance(version_payload.get("platformVariants"), dict) else {}
        variant_payload = platform_variants.get(platform) or version_payload
        if not isinstance(variant_payload, dict):
            variant_payload = {}
        return {**variant_payload, "platform": platform}

    def _normalize_hidden_elements(self, value: Any) -> dict | None:
        return value if isinstance(value, dict) else None

    def _normalize_question_block(self, value: Any) -> dict[str, Any]:
        if not isinstance(value, dict):
            return {"enabled": False, "type": "single", "questionText": "", "required": False, "options": []}
        options = value.get("options") if isinstance(value.get("options"), list) else []
        normalized_options = []
        for index, option in enumerate(options[:4], start=1):
            if isinstance(option, dict):
                label = str(option.get("label") or f"Option {index}").strip() or f"Option {index}"
            else:
                label = str(option or f"Option {index}").strip() or f"Option {index}"
            normalized_options.append({"label": label})
        question_text = str(value.get("questionText") or "").strip()
        enabled = bool(value.get("enabled")) if "enabled" in value else bool(question_text and normalized_options)
        if not enabled:
            normalized_options = []
            question_text = ""
        return {
            "enabled": enabled,
            "type": "multiple" if value.get("type") == "multiple" else "single",
            "questionText": question_text,
            "required": bool(value.get("required")),
            "options": normalized_options,
        }

    def _extract_question_text(self, value: Any) -> str | None:
        question_block = self._normalize_question_block(value)
        return self._empty_to_none(question_block.get("questionText"))

    def _extract_question_required(self, value: Any) -> bool:
        question_block = self._normalize_question_block(value)
        return bool(question_block.get("required"))

    def _generate_unique_invite_code(self, db: Session, length: int = 6) -> str:
        alphabet = string.ascii_uppercase + string.digits
        while True:
            candidate = "".join(secrets.choice(alphabet) for _ in range(length))
            exists = db.query(SurveyPublication).filter(SurveyPublication.invite_code == candidate).one_or_none()
            if exists is None:
                return candidate

    def _upsert_answers_from_payload(
        self,
        db: Session,
        session: ParticipantSession,
        publication: SurveyPublication,
        payload: dict[str, Any],
    ) -> None:
        answer_items = self._extract_answer_items(payload)
        if not answer_items:
            return

        news_items = {item.sort_order: item for item in publication.survey.news_items}
        existing = db.query(ParticipantAnswer).filter(ParticipantAnswer.session_id == session.id).all()
        for row in existing:
            db.delete(row)
        db.flush()

        for answer in answer_items:
            news_index = answer.get("newsIndex")
            option_id = answer.get("optionId")
            option_index = answer.get("optionIndex")
            news_item = news_items.get(news_index)
            if news_item is None:
                continue
            variant = self._pick_variant_for_publication(news_item, publication.published_version_key)
            if variant is None:
                continue
            option = None
            if option_id:
                option = next((item for item in variant.question_options if item.id == option_id), None)
            if option is None and isinstance(option_index, int):
                ordered_options = sorted(variant.question_options, key=lambda item: item.sort_order)
                if 0 <= option_index < len(ordered_options):
                    option = ordered_options[option_index]
            if option is None:
                continue

            db.add(
                ParticipantAnswer(
                    session_id=session.id,
                    news_item_id=news_item.id,
                    variant_id=variant.id,
                    option_id=option.id,
                    answered_at=utc_now(),
                )
            )
        db.flush()

    def _extract_answer_items(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        candidate_keys = ["answers", "responses", "questionResponses", "selectedAnswers"]
        for key in candidate_keys:
            value = payload.get(key)
            if isinstance(value, list):
                normalized: list[dict[str, Any]] = []
                for item in value:
                    if not isinstance(item, dict):
                        continue
                    news_index = item.get("newsIndex")
                    try:
                        news_index = int(news_index)
                    except (TypeError, ValueError):
                        continue
                    option_index = item.get("optionIndex")
                    try:
                        option_index = int(option_index) if option_index is not None else None
                    except (TypeError, ValueError):
                        option_index = None
                    normalized.append(
                        {
                            "newsIndex": news_index,
                            "optionId": str(item.get("optionId") or "").strip() or None,
                            "optionIndex": option_index,
                        }
                    )
                return normalized
        return []

    def _researcher_to_dict(self, obj: Researcher) -> dict[str, Any]:
        display_name = obj.username.split("@", 1)[0] or obj.username or "Researcher"
        return {
            "researcher_id": obj.id,
            "email": obj.username,
            "name": display_name,
            "initial": (display_name[:1] or "R").upper(),
            "created_at": obj.created_at.isoformat() if obj.created_at else None,
        }

    def _survey_to_dict(self, obj: Survey) -> dict[str, Any]:
        return {
            "survey_id": obj.id,
            "researcher_id": obj.researcher_id,
            "survey_title": obj.title,
            "status": obj.status,
            "created_at": obj.created_at.isoformat() if obj.created_at else None,
            "updated_at": obj.updated_at.isoformat() if obj.updated_at else None,
        }

    def _variant_to_legacy_dict(self, obj: SurveyVariant) -> dict[str, Any]:
        return {
            "survey_version_id": obj.id,
            "survey_id": obj.news_item.survey_id if obj.news_item else None,
            "version_label": obj.version_key,
            "platform": obj.platform,
            "caption": obj.caption,
            "image_url": obj.image_url,
            "likes_count": 0,
            "comments_count": 0,
            "shares_count": 0,
        }

    def _publication_to_dict(self, obj: SurveyPublication) -> dict[str, Any]:
        return {
            "publication_id": obj.id,
            "survey_id": obj.survey_id,
            "invite_code": obj.invite_code,
            "published_version_key": obj.published_version_key,
            "published_at": obj.published_at.isoformat() if obj.published_at else None,
        }

    def _publication_to_legacy_dict(self, obj: SurveyPublication, db: Session) -> dict[str, Any]:
        survey = obj.survey
        first_news = None
        variant = None
        if survey is not None and survey.news_items:
            first_news = sorted(survey.news_items, key=lambda item: item.sort_order)[0]
            variant = self._pick_variant_for_publication(first_news, obj.published_version_key)
        return {
            "publish_log_id": obj.id,
            "survey_id": obj.survey_id,
            "invite_code": obj.invite_code,
            "version_label": variant.version_key if variant else obj.published_version_key,
            "platform": variant.platform if variant else "instagram",
            "caption": variant.caption if variant else None,
            "image_url": variant.image_url if variant else None,
            "likes_count": 0,
            "comments_count": 0,
            "shares_count": 0,
            "published_at": obj.published_at.isoformat() if obj.published_at else None,
        }


db_bridge = DBBridge(auto_init=False)
