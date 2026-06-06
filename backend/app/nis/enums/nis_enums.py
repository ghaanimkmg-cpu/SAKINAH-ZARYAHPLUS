import enum

class VerificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"

class EligibilityStatus(str, enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    REJECTED = "REJECTED"
    BANNED = "BANNED"

class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class SafetyRiskLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class ConfidenceLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class MatchInterestStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    INTERESTED = "INTERESTED"
    PASSED = "PASSED"

class MatchflowStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CLOSED = "CLOSED"

class ConversationStatus(str, enum.Enum):
    OPEN = "OPEN"
    LOCKED = "LOCKED"
    CLOSED = "CLOSED"

class HumanReviewStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class HumanReviewDecision(str, enum.Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"

class SafetyFlagType(str, enum.Enum):
    HARASSMENT = "HARASSMENT"
    FRAUD = "FRAUD"
    INAPPROPRIATE = "INAPPROPRIATE"
    MANIPULATION_RISK = "MANIPULATION_RISK"
    AGGRESSIVE_LANGUAGE = "AGGRESSIVE_LANGUAGE"
    PHOTO_LEAK_RISK = "PHOTO_LEAK_RISK"
    BOUNDARY_PRESSURE = "BOUNDARY_PRESSURE"

class SafetySeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class CompatibilityStatus(str, enum.Enum):
    STRONG = "STRONG"
    MODERATE = "MODERATE"
    WEAK = "WEAK"
    INCOMPATIBLE = "INCOMPATIBLE"

class FinalMatchStatus(str, enum.Enum):
    MARRIED = "MARRIED"
    ENGAGED = "ENGAGED"
    ENDED = "ENDED"
