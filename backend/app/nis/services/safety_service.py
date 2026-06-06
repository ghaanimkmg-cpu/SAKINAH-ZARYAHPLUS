import uuid
from typing import Dict
from sqlalchemy.orm import Session
from app.nis.schemas.safety import ReportRequest, ReportResponse
from app.nis.services.human_review_service import NISHumanReviewService
from app.nis.models.safety import NISReport, NISSafetyFlag
from app.nis.enums.nis_enums import SafetyFlagType, SafetySeverity

class NISSafetyService:
    VALID_FLAGS = [
        "CONTACT_LEAK_ATTEMPT",
        "AGGRESSIVE_LANGUAGE",
        "MANIPULATION_RISK",
        "BOUNDARY_PRESSURE",
        "SUSPICIOUS_IDENTITY",
        "REPEATED_REPORTS",
        "MASS_INTEREST_BEHAVIOR",
        "OFF_PLATFORM_PRESSURE",
        "PHOTO_LEAK_RISK"
    ]

    VALID_SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    @classmethod
    def submit_report(cls, db: Session, reporter_id: str, request: ReportRequest) -> ReportResponse:
        if request.flag_type not in cls.VALID_FLAGS:
            raise ValueError("Invalid safety flag type.")
        if request.severity not in cls.VALID_SEVERITIES:
            raise ValueError("Invalid severity level.")

        try:
            flag_enum = SafetyFlagType[request.flag_type]
        except KeyError:
            flag_enum = SafetyFlagType.SUSPICIOUS_IDENTITY

        try:
            severity_enum = SafetySeverity[request.severity]
        except KeyError:
            severity_enum = SafetySeverity.LOW
            
        # Due to schema limitations, system users might not have UUIDs, so we fallback to a safe ID
        # or we just rely on string if Postgres allows. But SQLAlchemy UUID requires valid UUIDs.
        safe_reporter_id = reporter_id if len(reporter_id) >= 32 else uuid.uuid4().hex
        safe_target_id = request.reported_user_id if len(request.reported_user_id) >= 32 else uuid.uuid4().hex

        new_report = NISReport(
            reporter_id=uuid.UUID(hex=safe_reporter_id),
            target_id=uuid.UUID(hex=safe_target_id),
            reason=request.context or "No context provided"
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)

        report_count = db.query(NISReport).filter_by(target_id=uuid.UUID(hex=safe_target_id)).count()
        
        effective_severity = severity_enum
        if report_count >= 3 and effective_severity in [SafetySeverity.LOW, SafetySeverity.MEDIUM]:
            effective_severity = SafetySeverity.HIGH

        new_flag = NISSafetyFlag(
            reporter_id=uuid.UUID(hex=safe_reporter_id),
            target_id=uuid.UUID(hex=safe_target_id),
            flag_type=SafetyFlagType.REPEATED_REPORTS if report_count >= 3 else flag_enum,
            severity=effective_severity,
            description=request.context
        )
        db.add(new_flag)
        db.commit()

        requires_review = effective_severity in [SafetySeverity.HIGH, SafetySeverity.CRITICAL]
        if requires_review:
            NISHumanReviewService.create_review(db, str(new_flag.id), str(safe_target_id), effective_severity.name)

        return ReportResponse(
            report_id=str(new_report.id),
            status="RECEIVED",
            safety_flag_created=True,
            human_review_required=requires_review,
            message="Your report has been received and will be reviewed carefully."
        )

    @classmethod
    def log_contact_leak(cls, db: Session, user_id: str, context: str):
        req = ReportRequest(
            reported_user_id=user_id,
            flag_type="CONTACT_LEAK_ATTEMPT",
            severity="MEDIUM",
            context=context
        )
        # Fake UUID for system user
        system_uuid = uuid.uuid4().hex
        cls.submit_report(db, system_uuid, req)
