import uuid
import re
from typing import Dict
from app.nis.schemas.structured_conversation import (
    ConversationResponse, 
    ConversationTopic, 
    ConversationMessage,
    PostMessageResponse
)

_MOCK_CONVERSATIONS: Dict[str, dict] = {}
_MOCK_MATCHFLOW_STATES: Dict[str, str] = {}

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
    def get_or_create_conversation(cls, matchflow_id: str, user_id: str) -> str:
        mf_state = _MOCK_MATCHFLOW_STATES.get(matchflow_id)
        if not mf_state or mf_state not in ["STRUCTURED_OPENING", "SUPERVISED_DEPTH"]:
            raise ValueError("Conversation cannot start without valid matchflow permission.")
            
        for cid, conv in _MOCK_CONVERSATIONS.items():
            if conv["matchflow_id"] == matchflow_id:
                if user_id not in conv["users"]:
                    raise ValueError("Unauthorized")
                return cid

        conv_id = f"conv_{uuid.uuid4().hex[:8]}"
        _MOCK_CONVERSATIONS[conv_id] = {
            "matchflow_id": matchflow_id,
            "users": {user_id, "mock_other_user"},
            "current_topic": cls.PRE_NIKAH_TOPICS[0],
            "messages": [],
            "wali_present": False
        }
        return conv_id

    @classmethod
    def set_mock_users(cls, conv_id: str, users: list):
        if conv_id in _MOCK_CONVERSATIONS:
            _MOCK_CONVERSATIONS[conv_id]["users"] = set(users)

    @classmethod
    def get_conversation(cls, conversation_id: str, user_id: str) -> ConversationResponse:
        conv = _MOCK_CONVERSATIONS.get(conversation_id)
        if not conv:
            raise ValueError("Conversation not found.")
            
        if user_id not in conv["users"]:
            raise ValueError("Unauthorized access.")

        current_idx = cls.PRE_NIKAH_TOPICS.index(conv["current_topic"])
        topics_out = []
        for idx, t in enumerate(cls.PRE_NIKAH_TOPICS):
            if idx < current_idx:
                status = "DONE"
            elif idx == current_idx:
                status = "CURRENT"
            else:
                status = "LOCKED"
            topics_out.append(ConversationTopic(topic=t, status=status))

        return ConversationResponse(
            conversation_id=conversation_id,
            matchflow_id=conv["matchflow_id"],
            current_topic=conv["current_topic"],
            topics=topics_out,
            messages=conv["messages"],
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
    def post_message(cls, conversation_id: str, user_id: str, topic: str, content: str) -> PostMessageResponse:
        conv = _MOCK_CONVERSATIONS.get(conversation_id)
        if not conv:
            raise ValueError("Conversation not found.")
            
        if user_id not in conv["users"]:
            raise ValueError("Unauthorized access.")

        if topic != conv["current_topic"]:
            raise ValueError("Message must belong to the current active topic. Locked/past topics are invalid.")

        if cls.detect_contact_leak(content):
            return PostMessageResponse(
                accepted=False,
                contact_leak_detected=True,
                message="Please keep communication inside Sakinah for safety."
            )

        msg_id = f"msg_{uuid.uuid4().hex[:8]}"
        msg = ConversationMessage(
            message_id=msg_id,
            topic=topic,
            content=content,
            sender_id=user_id
        )
        conv["messages"].append(msg)

        return PostMessageResponse(
            message_id=msg_id,
            topic=topic,
            accepted=True,
            contact_leak_detected=False,
            message="Message recorded."
        )

    @classmethod
    def advance_topic(cls, conversation_id: str):
        conv = _MOCK_CONVERSATIONS.get(conversation_id)
        if not conv:
            raise ValueError("Conversation not found.")
        current_idx = cls.PRE_NIKAH_TOPICS.index(conv["current_topic"])
        if current_idx + 1 < len(cls.PRE_NIKAH_TOPICS):
            conv["current_topic"] = cls.PRE_NIKAH_TOPICS[current_idx + 1]

    @classmethod
    def clear_mock_state(cls):
        _MOCK_CONVERSATIONS.clear()
        _MOCK_MATCHFLOW_STATES.clear()

    @classmethod
    def seed_matchflow_state(cls, matchflow_id: str, state: str):
        _MOCK_MATCHFLOW_STATES[matchflow_id] = state
