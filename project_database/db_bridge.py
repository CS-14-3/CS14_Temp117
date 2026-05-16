from __future__ import annotations

import json
import secrets
import string
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy.orm import Session

from project_database.db import SessionLocal, init_db
from project_database.database_structure.auth_models import Researcher, ResearcherSession
from project_database.database_structure.survey_models import (
    Survey,
    SurveyPublishLog,
    SurveyVersion,
)
from project_database.database_structure.participant_models import (
    Participant,
    ParticipantInteractionLog,
    StudySession,
)
from project_database.database_structure.gaze_models import (
    CalibrationResult,
    CalibrationSample,
    GazePayloadArchive,
    GazeRecord,
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_email(value: Any) -> str:
    return str(value or "").strip().lower()


def normalize_invite_code(value: Any) -> str:
    allowed = string.ascii_uppercase + string.digits
    raw = str(value or "").upper()
    cleaned = "".join(ch for ch in raw if ch in allowed)
    return cleaned[:20]


def derive_display_name(email: str, fallback: str = "Researcher") -> str:
    local = email.split("@", 1)[0].strip()
    if not local:
        return fallback
    parts = [p for p in local.replace(".", " ").replace("_", " ").replace("-", " ").split() if p]
    if not parts:
        return fallback
    return " ".join(part[:1].upper() + part[1:] for part in parts[:2])


def safe_json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, default=str)


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
    """
    Thin database service layer for integrating the prototype with SQLAlchemy models.
    """

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
        normalized_email = normalize_email(email)
        password = str(password or "").strip()
        display_name = str(name or "").strip() or derive_display_name(normalized_email)

        if not normalized_email:
            raise ValueError("Email is required.")
        if not password:
            raise ValueError("Password is required.")

        with get_session() as db:
            existing = (
                db.query(Researcher)
                .filter(Researcher.email == normalized_email)
                .one_or_none()
            )

            if existing is not None:
                raise ValueError("This email is already registered.")

            researcher = Researcher(
                email=normalized_email,
                password=password,
                display_name=display_name,
                role=role,
                account_status="active",
            )
            db.add(researcher)
            db.flush()

            session_obj = self._create_session_record(
                db,
                researcher=researcher,
                ip_address=None,
                user_agent=None,
            )
            db.flush()

            return {
                "researcher_id": researcher.researcher_id,
                "email": researcher.email,
                "name": researcher.display_name,
                "initial": researcher.initial,
                "session_token": session_obj.session_token,
                "session_id": session_obj.session_id,
            }

    def login_researcher(
        self,
        *,
        email: str,
        password: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> dict[str, Any] | None:
        normalized_email = normalize_email(email)
        password = str(password or "").strip()

        with get_session() as db:
            researcher = (
                db.query(Researcher)
                .filter(Researcher.email == normalized_email)
                .one_or_none()
            )
            if researcher is None:
                return None
            if researcher.password != password:
                return None
            if researcher.account_status != "active":
                return None

            researcher.last_login_at = utc_now()

            session_obj = self._create_session_record(
                db,
                researcher=researcher,
                ip_address=ip_address,
                user_agent=user_agent,
            )
            db.flush()

            return {
                "researcher_id": researcher.researcher_id,
                "email": researcher.email,
                "name": researcher.display_name,
                "initial": researcher.initial,
                "session_token": session_obj.session_token,
                "session_id": session_obj.session_id,
            }

    def get_researcher_by_session_token(self, session_token: str) -> dict[str, Any] | None:
        token = str(session_token or "").strip()
        if not token:
            return None

        now = utc_now()
        with get_session() as db:
            session_obj = (
                db.query(ResearcherSession)
                .filter(ResearcherSession.session_token == token)
                .one_or_none()
            )
            if session_obj is None:
                return None
            if session_obj.is_revoked:
                return None
            if session_obj.expires_at <= now:
                return None

            session_obj.last_seen_at = now
            researcher = session_obj.researcher

            return {
                "researcher_id": researcher.researcher_id,
                "email": researcher.email,
                "name": researcher.display_name,
                "initial": researcher.initial,
                "session_token": session_obj.session_token,
                "session_id": session_obj.session_id,
            }

    def revoke_session(self, session_token: str) -> bool:
        token = str(session_token or "").strip()
        if not token:
            return False

        with get_session() as db:
            session_obj = (
                db.query(ResearcherSession)
                .filter(ResearcherSession.session_token == token)
                .one_or_none()
            )
            if session_obj is None:
                return False

            session_obj.is_revoked = True
            session_obj.last_seen_at = utc_now()
            return True

    def _create_session_record(
        self,
        db: Session,
        *,
        researcher: Researcher,
        ip_address: str | None,
        user_agent: str | None,
        ttl_hours: int = 8,
    ) -> ResearcherSession:
        token = secrets.token_urlsafe(32)
        now = utc_now()

        session_obj = ResearcherSession(
            researcher_id=researcher.researcher_id,
            session_token=token,
            issued_at=now,
            expires_at=now + timedelta(hours=ttl_hours),
            last_seen_at=now,
            ip_address=ip_address,
            user_agent=user_agent,
            is_revoked=False,
        )
        db.add(session_obj)
        return session_obj

    def get_researcher_by_email(self, email: str) -> dict[str, Any] | None:
        normalized_email = normalize_email(email)
        if not normalized_email:
            return None

        with get_session() as db:
            researcher = (
                db.query(Researcher)
                .filter(Researcher.email == normalized_email)
                .one_or_none()
            )
            if researcher is None:
                return None

            return {
                "researcher_id": researcher.researcher_id,
                "email": researcher.email,
                "name": researcher.display_name,
                "initial": researcher.initial,
                "role": researcher.role,
                "account_status": researcher.account_status,
            }    

    # ------------------------------------------------------------------
    # Survey / researcher main
    # ------------------------------------------------------------------

    def create_survey(
        self,
        *,
        researcher_id: str,
        survey_title: str | None = None,
        research_description: str | None = None,
        news_link: str | None = None,
        scraped_title: str | None = None,
        scraped_image_url: str | None = None,
    ) -> dict[str, Any]:
        with get_session() as db:
            survey = Survey(
                researcher_id=researcher_id,
                survey_title=survey_title,
                research_description=research_description,
                news_link=news_link,
                scraped_title=scraped_title,
                scraped_image_url=scraped_image_url,
                status="draft",
                is_published=False,
            )
            db.add(survey)
            db.flush()

            return self._survey_to_dict(survey)

    def update_survey(
        self,
        *,
        survey_id: str,
        survey_title: str | None = None,
        research_description: str | None = None,
        news_link: str | None = None,
        scraped_title: str | None = None,
        scraped_image_url: str | None = None,
        invite_code: str | None = None,
        survey_link: str | None = None,
        status: str | None = None,
        is_published: bool | None = None,
    ) -> dict[str, Any]:
        with get_session() as db:
            survey = db.query(Survey).filter(Survey.survey_id == survey_id).one_or_none()
            if survey is None:
                raise ValueError("Survey not found.")

            if survey_title is not None:
                survey.survey_title = survey_title
            if research_description is not None:
                survey.research_description = research_description
            if news_link is not None:
                survey.news_link = news_link
            if scraped_title is not None:
                survey.scraped_title = scraped_title
            if scraped_image_url is not None:
                survey.scraped_image_url = scraped_image_url
            if invite_code is not None:
                survey.invite_code = normalize_invite_code(invite_code)
            if survey_link is not None:
                survey.survey_link = survey_link
            if status is not None:
                survey.status = status
            if is_published is not None:
                survey.is_published = is_published

            db.flush()
            return self._survey_to_dict(survey)

    def upsert_survey_version(
        self,
        *,
        survey_id: str,
        version_label: str,
        platform: str,
        caption: str | None,
        image_url: str | None,
        likes_count: int = 0,
        comments_count: int = 0,
        shares_count: int = 0,
        is_default: bool = False,
    ) -> dict[str, Any]:
        label = str(version_label or "").strip()
        if not label:
            raise ValueError("version_label is required.")

        with get_session() as db:
            version = (
                db.query(SurveyVersion)
                .filter(
                    SurveyVersion.survey_id == survey_id,
                    SurveyVersion.version_label == label,
                )
                .one_or_none()
            )

            if version is None:
                version = SurveyVersion(
                    survey_id=survey_id,
                    version_label=label,
                )
                db.add(version)

            version.platform = str(platform or "instagram").strip().lower() or "instagram"
            version.caption = caption
            version.image_url = image_url
            version.likes_count = int(likes_count or 0)
            version.comments_count = int(comments_count or 0)
            version.shares_count = int(shares_count or 0)
            version.is_default = bool(is_default)

            if is_default:
                (
                    db.query(SurveyVersion)
                    .filter(
                        SurveyVersion.survey_id == survey_id,
                        SurveyVersion.version_label != label,
                    )
                    .update({"is_default": False}, synchronize_session=False)
                )

            db.flush()
            return self._survey_version_to_dict(version)

    def get_survey_with_versions(self, survey_id: str) -> dict[str, Any] | None:
        with get_session() as db:
            survey = db.query(Survey).filter(Survey.survey_id == survey_id).one_or_none()
            if survey is None:
                return None

            versions = (
                db.query(SurveyVersion)
                .filter(SurveyVersion.survey_id == survey.survey_id)
                .order_by(SurveyVersion.version_label.asc())
                .all()
            )

            data = self._survey_to_dict(survey)
            data["versions"] = [self._survey_version_to_dict(v) for v in versions]
            return data

    def publish_survey_version(
        self,
        *,
        survey_id: str,
        version_label: str,
        published_by_researcher_id: str | None,
        invite_code: str | None,
        participant_link: str | None,
    ) -> dict[str, Any]:
        label = str(version_label or "").strip()
        if not label:
            raise ValueError("version_label is required.")

        with get_session() as db:
            survey = db.query(Survey).filter(Survey.survey_id == survey_id).one_or_none()
            if survey is None:
                raise ValueError("Survey not found.")

            version = (
                db.query(SurveyVersion)
                .filter(
                    SurveyVersion.survey_id == survey_id,
                    SurveyVersion.version_label == label,
                )
                .one_or_none()
            )
            if version is None:
                raise ValueError("Survey version not found.")

            normalized_code = normalize_invite_code(invite_code) or self.generate_unique_invite_code(db)

            survey.invite_code = normalized_code
            survey.survey_link = participant_link
            survey.status = "published"
            survey.is_published = True

            publish_log = SurveyPublishLog(
                survey_id=survey.survey_id,
                survey_version_id=version.survey_version_id,
                published_by_researcher_id=published_by_researcher_id,
                invite_code=normalized_code,
                participant_link=participant_link,
                version_label=version.version_label,
                platform=version.platform,
                caption=version.caption,
                image_url=version.image_url,
                likes_count=version.likes_count,
                comments_count=version.comments_count,
                shares_count=version.shares_count,
            )
            db.add(publish_log)
            db.flush()

            return {
                "survey": self._survey_to_dict(survey),
                "version": self._survey_version_to_dict(version),
                "publish_log": self._publish_log_to_dict(publish_log),
            }

    def get_published_posts_by_invite_code(self, invite_code: str) -> list[dict[str, Any]]:
        normalized_code = normalize_invite_code(invite_code)
        if not normalized_code:
            return []

        with get_session() as db:
            logs = (
                db.query(SurveyPublishLog)
                .filter(SurveyPublishLog.invite_code == normalized_code)
                .order_by(SurveyPublishLog.published_at.asc())
                .all()
            )

            return [self._publish_log_to_participant_post(log) for log in logs]

    def generate_unique_invite_code(self, db: Session | None = None, length: int = 6) -> str:
        owns_session = db is None
        if owns_session:
            context = get_session()
            db_cm = context
            db = db_cm.__enter__()

        try:
            for _ in range(30):
                candidate = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))
                exists = (
                    db.query(SurveyPublishLog)
                    .filter(SurveyPublishLog.invite_code == candidate)
                    .first()
                )
                if exists is None:
                    return candidate
            return "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length + 2))
        finally:
            if owns_session:
                db_cm.__exit__(None, None, None)

    def get_survey_id_by_invite_code(self, invite_code: str) -> str | None:
        normalized_code = normalize_invite_code(invite_code)
        if not normalized_code:
            return None

        with get_session() as db:
            log = (
                db.query(SurveyPublishLog)
                .filter(SurveyPublishLog.invite_code == normalized_code)
                .order_by(SurveyPublishLog.published_at.desc())
                .first()
            )
            return log.survey_id if log else None
        
    def upsert_full_study_payload(
        self,
        *,
        participant_code: str,
        survey_id: str | None,
        invite_code: str | None,
        payload_type: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        with get_session() as db:
            participant = (
                db.query(Participant)
                .filter(Participant.participant_code == participant_code)
                .one_or_none()
            )
            if participant is None:
                participant = Participant(participant_code=participant_code)
                db.add(participant)
                db.flush()

            started_at = self._iso_to_datetime(payload.get("startedAt")) or utc_now()
            normalized_invite = normalize_invite_code(invite_code)

            study_session = (
                db.query(StudySession)
                .filter(
                    StudySession.participant_id == participant.participant_id,
                    StudySession.started_at == started_at,
                )
                .one_or_none()
            )

            if study_session is None:
                study_session = StudySession(
                    participant_id=participant.participant_id,
                    survey_id=survey_id,
                    invite_code=normalized_invite,
                    session_status="completed" if payload.get("studyEndedAt") else "started",
                    started_at=started_at,
                    calibration_started_at=self._iso_to_datetime(payload.get("startedAt")),
                    calibration_completed_at=self._iso_to_datetime(payload.get("studyStartedAt")),
                    study_started_at=self._iso_to_datetime(payload.get("studyStartedAt")),
                    study_ended_at=self._iso_to_datetime(payload.get("studyEndedAt")),
                    exported_at=None,
                )
                db.add(study_session)
                db.flush()
            else:
                study_session.survey_id = survey_id
                study_session.invite_code = normalized_invite
                study_session.session_status = "completed" if payload.get("studyEndedAt") else "started"
                study_session.calibration_started_at = self._iso_to_datetime(payload.get("startedAt"))
                study_session.calibration_completed_at = self._iso_to_datetime(payload.get("studyStartedAt"))
                study_session.study_started_at = self._iso_to_datetime(payload.get("studyStartedAt"))
                study_session.study_ended_at = self._iso_to_datetime(payload.get("studyEndedAt"))

            # 覆盖结构化子数据，避免 autosave 重复堆积
            db.query(ParticipantInteractionLog).filter(
                ParticipantInteractionLog.study_session_id == study_session.study_session_id
            ).delete(synchronize_session=False)

            existing_results = (
                db.query(CalibrationResult)
                .filter(CalibrationResult.study_session_id == study_session.study_session_id)
                .all()
            )
            for result in existing_results:
                db.delete(result)

            db.query(GazeRecord).filter(
                GazeRecord.study_session_id == study_session.study_session_id
            ).delete(synchronize_session=False)

            # interaction logs
            interaction_count = 0
            for item in payload.get("interactionLogs", []):
                log = ParticipantInteractionLog(
                    study_session_id=study_session.study_session_id,
                    event_type=str(item.get("type") or item.get("event_type") or "unknown"),
                    post_id=str(item.get("postId") or item.get("post_id") or "") or None,
                    view_mode=str(item.get("viewMode") or item.get("view_mode") or "") or None,
                    event_timestamp=self._ts_to_datetime(item.get("t")) or utc_now(),
                    event_payload=safe_json_dumps(item),
                )
                db.add(log)
                interaction_count += 1

            # calibration result + samples
            quality_metrics = payload.get("qualityMetrics") or {}
            calibration_logs = payload.get("calibrationLogs") or []

            calibration_result_id = None
            calibration_sample_count = 0

            if quality_metrics or calibration_logs:
                calibration_result = CalibrationResult(
                    study_session_id=study_session.study_session_id,
                    overall_score=self._to_float(quality_metrics.get("overall")),
                    score_percent=self._to_int(quality_metrics.get("scorePercent")),
                    passed=bool(quality_metrics.get("pass", False)),
                    quality_threshold=self._to_float(quality_metrics.get("quality_threshold")),
                    total_points=self._infer_total_points(quality_metrics, calibration_logs),
                    raw_quality_metrics=safe_json_dumps(quality_metrics),
                )
                db.add(calibration_result)
                db.flush()
                calibration_result_id = calibration_result.calibration_result_id

                for item in calibration_logs:
                    target = item.get("target") or {}
                    sample = CalibrationSample(
                        calibration_result_id=calibration_result.calibration_result_id,
                        study_session_id=study_session.study_session_id,
                        target_index=self._to_int(item.get("targetIdx")),
                        target_x=self._to_float(target.get("x")),
                        target_y=self._to_float(target.get("y")),
                        iris_x=self._to_float(item.get("irisX")),
                        iris_y=self._to_float(item.get("irisY")),
                        sample_timestamp=self._ts_to_datetime(item.get("t")) or utc_now(),
                    )
                    db.add(sample)
                    calibration_sample_count += 1

            # gaze records
            gaze_count = 0
            for item in payload.get("gazeLogs", []):
                record = GazeRecord(
                    study_session_id=study_session.study_session_id,
                    survey_id=survey_id,
                    post_id=str(item.get("postId") or item.get("post_id") or "") or None,
                    view_mode=str(item.get("viewMode") or item.get("view_mode") or "") or None,
                    iris_x=self._to_float(item.get("irisX")),
                    iris_y=self._to_float(item.get("irisY")),
                    iris_z=self._to_float(item.get("irisZ")),
                    face_detected=bool(item.get("faceDetected", False)),
                    gaze_region=str(item.get("gazedRegion") or "") or None,
                    screen_x=self._to_float(item.get("screenX")),
                    screen_y=self._to_float(item.get("screenY")),
                    recorded_at=self._ts_to_datetime(item.get("t")) or utc_now(),
                )
                db.add(record)
                gaze_count += 1

            # 保留 archive 历史
            archive = GazePayloadArchive(
                study_session_id=study_session.study_session_id,
                payload_type=str(payload_type or "study"),
                payload_json=safe_json_dumps(payload),
            )
            db.add(archive)
            db.flush()

            return {
                "participant_id": participant.participant_id,
                "study_session_id": study_session.study_session_id,
                "calibration_result_id": calibration_result_id,
                "interaction_logs_saved": interaction_count,
                "calibration_samples_saved": calibration_sample_count,
                "gaze_records_saved": gaze_count,
                "payload_archive_id": archive.payload_archive_id,
            }

    # ------------------------------------------------------------------
    # Participant / study session
    # ------------------------------------------------------------------

    def get_or_create_participant(self, participant_code: str) -> dict[str, Any]:
        code = str(participant_code or "").strip()
        if not code:
            raise ValueError("participant_code is required.")

        with get_session() as db:
            participant = (
                db.query(Participant)
                .filter(Participant.participant_code == code)
                .one_or_none()
            )
            if participant is None:
                participant = Participant(participant_code=code)
                db.add(participant)
                db.flush()

            return self._participant_to_dict(participant)

    def create_study_session(
        self,
        *,
        participant_code: str,
        survey_id: str | None,
        invite_code: str | None,
        session_status: str = "started",
        started_at: datetime | None = None,
    ) -> dict[str, Any]:
        with get_session() as db:
            participant = (
                db.query(Participant)
                .filter(Participant.participant_code == participant_code)
                .one_or_none()
            )
            if participant is None:
                participant = Participant(participant_code=participant_code)
                db.add(participant)
                db.flush()

            study_session = StudySession(
                participant_id=participant.participant_id,
                survey_id=survey_id,
                invite_code=normalize_invite_code(invite_code),
                session_status=session_status,
                started_at=started_at or utc_now(),
            )
            db.add(study_session)
            db.flush()

            return self._study_session_to_dict(study_session)

    def update_study_session(
        self,
        *,
        study_session_id: str,
        session_status: str | None = None,
        started_at: datetime | None = None,
        calibration_started_at: datetime | None = None,
        calibration_completed_at: datetime | None = None,
        study_started_at: datetime | None = None,
        study_ended_at: datetime | None = None,
        exported_at: datetime | None = None,
    ) -> dict[str, Any]:
        with get_session() as db:
            study_session = (
                db.query(StudySession)
                .filter(StudySession.study_session_id == study_session_id)
                .one_or_none()
            )
            if study_session is None:
                raise ValueError("Study session not found.")

            if session_status is not None:
                study_session.session_status = session_status
            if started_at is not None:
                study_session.started_at = started_at
            if calibration_started_at is not None:
                study_session.calibration_started_at = calibration_started_at
            if calibration_completed_at is not None:
                study_session.calibration_completed_at = calibration_completed_at
            if study_started_at is not None:
                study_session.study_started_at = study_started_at
            if study_ended_at is not None:
                study_session.study_ended_at = study_ended_at
            if exported_at is not None:
                study_session.exported_at = exported_at

            db.flush()
            return self._study_session_to_dict(study_session)

    def save_interaction_logs(
        self,
        *,
        study_session_id: str,
        logs: list[dict[str, Any]],
    ) -> int:
        if not logs:
            return 0

        with get_session() as db:
            count = 0
            for item in logs:
                log = ParticipantInteractionLog(
                    study_session_id=study_session_id,
                    event_type=str(item.get("type") or item.get("event_type") or "unknown"),
                    post_id=str(item.get("postId") or item.get("post_id") or "") or None,
                    view_mode=str(item.get("viewMode") or item.get("view_mode") or "") or None,
                    event_timestamp=self._ts_to_datetime(item.get("t")) or utc_now(),
                    event_payload=safe_json_dumps(item),
                )
                db.add(log)
                count += 1

            return count

    # ------------------------------------------------------------------
    # Calibration / gaze
    # ------------------------------------------------------------------

    def save_calibration_result_with_samples(
        self,
        *,
        study_session_id: str,
        quality_metrics: dict[str, Any] | None,
        calibration_logs: list[dict[str, Any]] | None,
        quality_threshold: float | None = None,
        total_points: int | None = None,
    ) -> dict[str, Any]:
        quality_metrics = quality_metrics or {}
        calibration_logs = calibration_logs or []

        with get_session() as db:
            result = CalibrationResult(
                study_session_id=study_session_id,
                overall_score=self._to_float(quality_metrics.get("overall")),
                score_percent=self._to_int(quality_metrics.get("scorePercent")),
                passed=bool(quality_metrics.get("pass", False)),
                quality_threshold=quality_threshold if quality_threshold is not None else self._to_float(quality_metrics.get("quality_threshold")),
                total_points=total_points if total_points is not None else self._infer_total_points(quality_metrics, calibration_logs),
                raw_quality_metrics=safe_json_dumps(quality_metrics),
            )
            db.add(result)
            db.flush()

            samples_saved = 0
            for item in calibration_logs:
                target = item.get("target") or {}
                sample = CalibrationSample(
                    calibration_result_id=result.calibration_result_id,
                    study_session_id=study_session_id,
                    target_index=self._to_int(item.get("targetIdx")),
                    target_x=self._to_float(target.get("x")),
                    target_y=self._to_float(target.get("y")),
                    iris_x=self._to_float(item.get("irisX")),
                    iris_y=self._to_float(item.get("irisY")),
                    sample_timestamp=self._ts_to_datetime(item.get("t")) or utc_now(),
                )
                db.add(sample)
                samples_saved += 1

            db.flush()
            return {
                "calibration_result_id": result.calibration_result_id,
                "samples_saved": samples_saved,
            }

    def save_gaze_records(
        self,
        *,
        study_session_id: str,
        survey_id: str | None,
        gaze_logs: list[dict[str, Any]],
    ) -> int:
        if not gaze_logs:
            return 0

        with get_session() as db:
            count = 0
            for item in gaze_logs:
                record = GazeRecord(
                    study_session_id=study_session_id,
                    survey_id=survey_id,
                    post_id=str(item.get("postId") or item.get("post_id") or "") or None,
                    view_mode=str(item.get("viewMode") or item.get("view_mode") or "") or None,
                    iris_x=self._to_float(item.get("irisX")),
                    iris_y=self._to_float(item.get("irisY")),
                    iris_z=self._to_float(item.get("irisZ")),
                    face_detected=bool(item.get("faceDetected", False)),
                    gaze_region=str(item.get("gazedRegion") or "") or None,
                    screen_x=self._to_float(item.get("screenX")),
                    screen_y=self._to_float(item.get("screenY")),
                    recorded_at=self._ts_to_datetime(item.get("t")) or utc_now(),
                )
                db.add(record)
                count += 1

            return count

    def archive_payload(
        self,
        *,
        study_session_id: str,
        payload_type: str,
        payload: dict[str, Any] | list[Any] | str,
    ) -> dict[str, Any]:
        payload_json = payload if isinstance(payload, str) else safe_json_dumps(payload)

        with get_session() as db:
            archive = GazePayloadArchive(
                study_session_id=study_session_id,
                payload_type=str(payload_type or "unknown"),
                payload_json=payload_json,
            )
            db.add(archive)
            db.flush()

            return {
                "payload_archive_id": archive.payload_archive_id,
                "saved_at": archive.saved_at.isoformat() if archive.saved_at else None,
            }

    def save_full_study_payload(
        self,
        *,
        participant_code: str,
        survey_id: str | None,
        invite_code: str | None,
        payload_type: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Convenience method for participant/backend integration:
        1) ensure participant exists
        2) create a study_session
        3) save interaction logs
        4) save calibration result + samples
        5) save gaze records
        6) archive the full raw payload
        """
        with get_session() as db:
            participant = (
                db.query(Participant)
                .filter(Participant.participant_code == participant_code)
                .one_or_none()
            )
            if participant is None:
                participant = Participant(participant_code=participant_code)
                db.add(participant)
                db.flush()

            study_session = StudySession(
                participant_id=participant.participant_id,
                survey_id=survey_id,
                invite_code=normalize_invite_code(invite_code),
                session_status="completed" if payload.get("studyEndedAt") else "started",
                started_at=self._iso_to_datetime(payload.get("startedAt")) or utc_now(),
                calibration_started_at=self._iso_to_datetime(payload.get("startedAt")),
                calibration_completed_at=self._iso_to_datetime(payload.get("studyStartedAt")),
                study_started_at=self._iso_to_datetime(payload.get("studyStartedAt")),
                study_ended_at=self._iso_to_datetime(payload.get("studyEndedAt")),
                exported_at=None,
            )
            db.add(study_session)
            db.flush()

            interaction_count = 0
            for item in payload.get("interactionLogs", []):
                log = ParticipantInteractionLog(
                    study_session_id=study_session.study_session_id,
                    event_type=str(item.get("type") or item.get("event_type") or "unknown"),
                    post_id=str(item.get("postId") or item.get("post_id") or "") or None,
                    view_mode=str(item.get("viewMode") or item.get("view_mode") or "") or None,
                    event_timestamp=self._ts_to_datetime(item.get("t")) or utc_now(),
                    event_payload=safe_json_dumps(item),
                )
                db.add(log)
                interaction_count += 1

            quality_metrics = payload.get("qualityMetrics") or {}
            calibration_logs = payload.get("calibrationLogs") or []

            calibration_result = CalibrationResult(
                study_session_id=study_session.study_session_id,
                overall_score=self._to_float(quality_metrics.get("overall")),
                score_percent=self._to_int(quality_metrics.get("scorePercent")),
                passed=bool(quality_metrics.get("pass", False)),
                quality_threshold=self._to_float(quality_metrics.get("quality_threshold")),
                total_points=self._infer_total_points(quality_metrics, calibration_logs),
                raw_quality_metrics=safe_json_dumps(quality_metrics),
            )
            db.add(calibration_result)
            db.flush()

            calibration_sample_count = 0
            for item in calibration_logs:
                target = item.get("target") or {}
                sample = CalibrationSample(
                    calibration_result_id=calibration_result.calibration_result_id,
                    study_session_id=study_session.study_session_id,
                    target_index=self._to_int(item.get("targetIdx")),
                    target_x=self._to_float(target.get("x")),
                    target_y=self._to_float(target.get("y")),
                    iris_x=self._to_float(item.get("irisX")),
                    iris_y=self._to_float(item.get("irisY")),
                    sample_timestamp=self._ts_to_datetime(item.get("t")) or utc_now(),
                )
                db.add(sample)
                calibration_sample_count += 1

            gaze_count = 0
            for item in payload.get("gazeLogs", []):
                record = GazeRecord(
                    study_session_id=study_session.study_session_id,
                    survey_id=survey_id,
                    post_id=str(item.get("postId") or item.get("post_id") or "") or None,
                    view_mode=str(item.get("viewMode") or item.get("view_mode") or "") or None,
                    iris_x=self._to_float(item.get("irisX")),
                    iris_y=self._to_float(item.get("irisY")),
                    iris_z=self._to_float(item.get("irisZ")),
                    face_detected=bool(item.get("faceDetected", False)),
                    gaze_region=str(item.get("gazedRegion") or "") or None,
                    screen_x=self._to_float(item.get("screenX")),
                    screen_y=self._to_float(item.get("screenY")),
                    recorded_at=self._ts_to_datetime(item.get("t")) or utc_now(),
                )
                db.add(record)
                gaze_count += 1

            archive = GazePayloadArchive(
                study_session_id=study_session.study_session_id,
                payload_type=str(payload_type or "study"),
                payload_json=safe_json_dumps(payload),
            )
            db.add(archive)
            db.flush()

            return {
                "participant_id": participant.participant_id,
                "study_session_id": study_session.study_session_id,
                "interaction_logs_saved": interaction_count,
                "calibration_samples_saved": calibration_sample_count,
                "gaze_records_saved": gaze_count,
                "payload_archive_id": archive.payload_archive_id,
            }

    # ------------------------------------------------------------------
    # Internal serializers
    # ------------------------------------------------------------------

    def _researcher_to_dict(self, obj: Researcher) -> dict[str, Any]:
        return {
            "researcher_id": obj.researcher_id,
            "email": obj.email,
            "display_name": obj.display_name,
            "role": obj.role,
            "account_status": obj.account_status,
            "created_at": obj.created_at.isoformat() if obj.created_at else None,
            "updated_at": obj.updated_at.isoformat() if obj.updated_at else None,
            "last_login_at": obj.last_login_at.isoformat() if obj.last_login_at else None,
        }

    def _survey_to_dict(self, obj: Survey) -> dict[str, Any]:
        return {
            "survey_id": obj.survey_id,
            "researcher_id": obj.researcher_id,
            "survey_title": obj.survey_title,
            "research_description": obj.research_description,
            "news_link": obj.news_link,
            "scraped_title": obj.scraped_title,
            "scraped_image_url": obj.scraped_image_url,
            "invite_code": obj.invite_code,
            "survey_link": obj.survey_link,
            "status": obj.status,
            "is_published": obj.is_published,
            "created_at": obj.created_at.isoformat() if obj.created_at else None,
            "updated_at": obj.updated_at.isoformat() if obj.updated_at else None,
        }

    def _survey_version_to_dict(self, obj: SurveyVersion) -> dict[str, Any]:
        return {
            "survey_version_id": obj.survey_version_id,
            "survey_id": obj.survey_id,
            "version_label": obj.version_label,
            "is_default": obj.is_default,
            "platform": obj.platform,
            "caption": obj.caption,
            "image_url": obj.image_url,
            "likes_count": obj.likes_count,
            "comments_count": obj.comments_count,
            "shares_count": obj.shares_count,
            "created_at": obj.created_at.isoformat() if obj.created_at else None,
            "updated_at": obj.updated_at.isoformat() if obj.updated_at else None,
        }

    def _publish_log_to_dict(self, obj: SurveyPublishLog) -> dict[str, Any]:
        return {
            "publish_log_id": obj.publish_log_id,
            "survey_id": obj.survey_id,
            "survey_version_id": obj.survey_version_id,
            "published_by_researcher_id": obj.published_by_researcher_id,
            "invite_code": obj.invite_code,
            "participant_link": obj.participant_link,
            "version_label": obj.version_label,
            "platform": obj.platform,
            "caption": obj.caption,
            "image_url": obj.image_url,
            "likes_count": obj.likes_count,
            "comments_count": obj.comments_count,
            "shares_count": obj.shares_count,
            "published_at": obj.published_at.isoformat() if obj.published_at else None,
        }

    def _publish_log_to_participant_post(self, obj: SurveyPublishLog) -> dict[str, Any]:
        username = "sydney_news_hub"
        return {
            "id": obj.publish_log_id,
            "inviteCode": obj.invite_code,
            "platform": obj.platform,
            "caption": obj.caption or "",
            "image": obj.image_url or "",
            "likes": obj.likes_count or 0,
            "comments": obj.comments_count or 0,
            "shares": obj.shares_count or 0,
            "version": obj.version_label or "",
            "username": username,
            "location": "Sydney, Australia",
            "time": "Just now",
            "previewLabel": "" if obj.image_url else "[News Image Preview]",
            "avatarLetter": (username[:1] or "S").upper(),
            "commentsList": [
                "This post was published from the researcher prototype.",
                f"Platform mapping: {str(obj.platform or 'instagram').lower()}.",
            ],
        }

    def _participant_to_dict(self, obj: Participant) -> dict[str, Any]:
        return {
            "participant_id": obj.participant_id,
            "participant_code": obj.participant_code,
            "created_at": obj.created_at.isoformat() if obj.created_at else None,
        }

    def _study_session_to_dict(self, obj: StudySession) -> dict[str, Any]:
        return {
            "study_session_id": obj.study_session_id,
            "participant_id": obj.participant_id,
            "survey_id": obj.survey_id,
            "invite_code": obj.invite_code,
            "session_status": obj.session_status,
            "started_at": obj.started_at.isoformat() if obj.started_at else None,
            "calibration_started_at": obj.calibration_started_at.isoformat() if obj.calibration_started_at else None,
            "calibration_completed_at": obj.calibration_completed_at.isoformat() if obj.calibration_completed_at else None,
            "study_started_at": obj.study_started_at.isoformat() if obj.study_started_at else None,
            "study_ended_at": obj.study_ended_at.isoformat() if obj.study_ended_at else None,
            "exported_at": obj.exported_at.isoformat() if obj.exported_at else None,
            "created_at": obj.created_at.isoformat() if obj.created_at else None,
            "updated_at": obj.updated_at.isoformat() if obj.updated_at else None,
        }

    # ------------------------------------------------------------------
    # Conversion helpers
    # ------------------------------------------------------------------

    def _to_float(self, value: Any) -> float | None:
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _to_int(self, value: Any) -> int | None:
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _ts_to_datetime(self, value: Any) -> datetime | None:
        if value is None:
            return None
        try:
            return datetime.fromtimestamp(float(value) / 1000, tz=timezone.utc)
        except (TypeError, ValueError, OSError):
            return None

    def _iso_to_datetime(self, value: Any) -> datetime | None:
        text = str(value or "").strip()
        if not text:
            return None
        try:
            if text.endswith("Z"):
                text = text[:-1] + "+00:00"
            dt = datetime.fromisoformat(text)
            if dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            return None

    def _infer_total_points(
        self,
        quality_metrics: dict[str, Any],
        calibration_logs: list[dict[str, Any]],
    ) -> int | None:
        per_point = quality_metrics.get("perPoint")
        if isinstance(per_point, list):
            return len(per_point)

        indices = {
            self._to_int(item.get("targetIdx"))
            for item in calibration_logs
            if self._to_int(item.get("targetIdx")) is not None
        }
        return len(indices) if indices else None


db_bridge = DBBridge(auto_init=False)