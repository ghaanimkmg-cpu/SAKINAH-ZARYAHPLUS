import enum

class VerificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"

class EligibilityStatus(str, enum.Enum):
    ELIGIBLE = "ELIGIBLE"
    INELIGIBLE = "INELIGIBLE"
    NEEDS_REVIEW = "NEEDS_REVIEW"

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
