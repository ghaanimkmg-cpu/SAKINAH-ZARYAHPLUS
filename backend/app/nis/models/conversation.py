from sqlalchemy import Column, String, Enum as SQLEnum, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.nis.models.base import NISBaseModel
from app.nis.enums.nis_enums import ConversationStatus

class NISStructuredConversation(NISBaseModel):
    __tablename__ = "nis_structured_conversations"
    matchflow_id = Column(UUID(as_uuid=True), ForeignKey("nis_matchflows.id"), unique=True, nullable=False)
    status = Column(SQLEnum(ConversationStatus), default=ConversationStatus.LOCKED)
    topic_unlocked = Column(String, nullable=True)

class NISConversationMessage(NISBaseModel):
    __tablename__ = "nis_conversation_messages"
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("nis_structured_conversations.id"), nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_system_message = Column(Boolean, default=False)
