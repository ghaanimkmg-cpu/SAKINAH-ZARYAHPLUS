import uuid
import re
from typing import Dict
from sqlalchemy.orm import Session
from app.nis.schemas.structured_conversation import (
    ConversationResponse, 
    ConversationTopic, 
    ConversationMessage as SchemaConversationMessage,
    PostMessageResponse
)
from app.nis.models.conversation import NISStructuredConversation, NISConversationMessage
from app.nis.models.matching import NISMatchflow
from app.nis.enums.nis_enums import MatchflowStatus

class NISStructuredConversationService:
    PRE_NIKAH_TOPICS = [
        "PARENTS_AND_FAMILY",
        "WORK",
        "FRIENDS",
        "HABITS",
        "SELF_IMAGE",
        "RESPONSIBILITY",
        "EXPECTATIONS",
        "FINANCES"
    ]

    CONTACT_REGEX = [
        r"\b\d{7,15}\b",
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        r"instagram\.com",
        r"ig\s*handle",
        r"whatsapp",
        r"telegram",
        r"http[s]?://",
        r"call me",
        r"text me",
        r"message me outside",
        r"dm me",
        r"@"
    ]

    @classmethod
    def get_or_create_conversation(cls, db: Session, matchflow_id: str, user_id: str) -> str:
        try:
            mf_uuid = uuid.UUID(matchflow_id)
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise ValueError("Invalid UUID format.")
            
        mf = db.query(NISMatchflow).filter_by(id=mf_uuid).first()
        if not mf or mf.current_step not in ["STRUCTURED_OPENING", "SUPERVISED_DEPTH"]:
            raise ValueError("Conversation cannot start without valid matchflow permission.")
            
        if user_uuid not in [mf.user_a_id, mf.user_b_id]:
            raise ValueError("Unauthorized")
            
        conv = db.query(NISStructuredConversation).filter_by(matchflow_id=mf_uuid).first()
        if conv:
            return str(conv.id)

        conv = NISStructuredConversation(
            matchflow_id=mf_uuid,
            current_topic=cls.PRE_NIKAH_TOPICS[0]
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)
        return str(conv.id)

    @classmethod
    def get_conversation(cls, db: Session, conversation_id: str, user_id: str) -> ConversationResponse:
        try:
            conv_uuid = uuid.UUID(conversation_id)
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise ValueError("Invalid UUID format.")
            
        conv = db.query(NISStructuredConversation).filter_by(id=conv_uuid).first()
        if not conv:
            raise ValueError("Conversation not found.")
            
        mf = db.query(NISMatchflow).filter_by(id=conv.matchflow_id).first()
        if not mf or user_uuid not in [mf.user_a_id, mf.user_b_id]:
            raise ValueError("Unauthorized access.")

        current_idx = cls.PRE_NIKAH_TOPICS.index(conv.current_topic or cls.PRE_NIKAH_TOPICS[0])
        topics_out = []
        for idx, t in enumerate(cls.PRE_NIKAH_TOPICS):
            if idx < current_idx:
                status = "DONE"
            elif idx == current_idx:
                status = "CURRENT"
            else:
                status = "LOCKED"
            topics_out.append(ConversationTopic(topic=t, status=status))

        messages = db.query(NISConversationMessage).filter_by(conversation_id=conv.id).all()
        msg_out = [
            SchemaConversationMessage(
                message_id=str(m.id),
                topic=m.topic,
                content=m.content,
                sender_id=str(m.sender_id)
            ) for m in messages
        ]

        return ConversationResponse(
            conversation_id=conversation_id,
            matchflow_id=str(conv.matchflow_id),
            current_topic=conv.current_topic,
            topics=topics_out,
            messages=msg_out,
            contact_warning="Please keep communication inside Sakinah until the guided process allows the next step."
        )

    @classmethod
    def detect_contact_leak(cls, text: str) -> bool:
        lower_text = text.lower()
        for pattern in cls.CONTACT_REGEX:
            if re.search(pattern, lower_text):
                return True
        return False

    @classmethod
    def post_message(cls, db: Session, conversation_id: str, user_id: str, topic: str, content: str) -> PostMessageResponse:
        try:
            conv_uuid = uuid.UUID(conversation_id)
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise ValueError("Invalid UUID format.")
            
        conv = db.query(NISStructuredConversation).filter_by(id=conv_uuid).first()
        if not conv:
            raise ValueError("Conversation not found.")
            
        mf = db.query(NISMatchflow).filter_by(id=conv.matchflow_id).first()
        if not mf or user_uuid not in [mf.user_a_id, mf.user_b_id]:
            raise ValueError("Unauthorized access.")

        if topic != conv.current_topic:
            raise ValueError("Message must belong to the current active topic. Locked/past topics are invalid.")

        if cls.detect_contact_leak(content):
            return PostMessageResponse(
                accepted=False,
                contact_leak_detected=True,
                message="Please keep communication inside Sakinah for safety."
            )

        msg = NISConversationMessage(
            conversation_id=conv.id,
            sender_id=user_uuid,
            topic=topic,
            content=content
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)

        return PostMessageResponse(
            message_id=str(msg.id),
            topic=topic,
            accepted=True,
            contact_leak_detected=False,
            message="Message recorded."
        )

    @classmethod
    def advance_topic(cls, db: Session, conversation_id: str):
        try:
            conv_uuid = uuid.UUID(conversation_id)
        except ValueError:
            raise ValueError("Invalid UUID format.")
            
        conv = db.query(NISStructuredConversation).filter_by(id=conv_uuid).first()
        if not conv:
            raise ValueError("Conversation not found.")
            
        current_idx = cls.PRE_NIKAH_TOPICS.index(conv.current_topic or cls.PRE_NIKAH_TOPICS[0])
        if current_idx + 1 < len(cls.PRE_NIKAH_TOPICS):
            conv.current_topic = cls.PRE_NIKAH_TOPICS[current_idx + 1]
            db.commit()

    @classmethod
    def set_mock_users(cls, conv_id: str, users: list):
        pass # Not needed in DB version

    @classmethod
    def clear_mock_state(cls):
        pass # Not needed in DB version
        
    @classmethod
    def seed_matchflow_state(cls, matchflow_id: str, state: str):
        pass # Not needed in DB version
