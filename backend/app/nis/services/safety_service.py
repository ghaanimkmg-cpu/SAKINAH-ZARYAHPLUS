import uuid
from typing import Dict
from app.nis.schemas.safety import ReportRequest, ReportResponse
from app.nis.services.human_review_service import NISHumanReviewService

_MOCK_REPORTS_DB: Dict[str, dict] = {}
_MOCK_SAFETY_FLAGS: Dict[str, dict] = {}

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
    def submit_report(cls, reporter_id: str, request: ReportRequest) -> ReportResponse:
        if request.flag_type not in cls.VALID_FLAGS:
            raise ValueError("Invalid safety flag type.")
        if request.severity not in cls.VALID_SEVERITIES:
            raise ValueError("Invalid severity level.")

        report_id = f"rep_{uuid.uuid4().hex[:8]}"
        flag_id = f"flag_{uuid.uuid4().hex[:8]}"
        
        _MOCK_REPORTS_DB[report_id] = {
            "reporter_id": reporter_id,
            "reported_user_id": request.reported_user_id,
            "flag_type": request.flag_type,
            "severity": request.severity,
            "context": request.context
        }

        report_count = sum(1 for r in _MOCK_REPORTS_DB.values() if r["reported_user_id"] == request.reported_user_id)
        
        effective_severity = request.severity
        if report_count >= 3 and effective_severity in ["LOW", "MEDIUM"]:
            effective_severity = "HIGH"
            _MOCK_SAFETY_FLAGS[flag_id] = {"type": "REPEATED_REPORTS", "user": request.reported_user_id}

        _MOCK_SAFETY_FLAGS[flag_id] = {
            "type": request.flag_type,
            "severity": effective_severity,
            "user": request.reported_user_id
        }

        requires_review = effective_severity in ["HIGH", "CRITICAL"]
        if requires_review:
            NISHumanReviewService.create_review(flag_id, request.reported_user_id, effective_severity)

        return ReportResponse(
            report_id=report_id,
            status="RECEIVED",
            safety_flag_created=True,
            human_review_required=requires_review,
            message="Your report has been received and will be reviewed carefully."
        )

    @classmethod
    def log_contact_leak(cls, user_id: str, context: str):
        req = ReportRequest(
            reported_user_id=user_id,
            flag_type="CONTACT_LEAK_ATTEMPT",
            severity="MEDIUM",
            context=context
        )
        cls.submit_report("system", req)

    @classmethod
    def clear_mock_state(cls):
        _MOCK_REPORTS_DB.clear()
        _MOCK_SAFETY_FLAGS.clear()
