from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class ConversationTopic(BaseModel):
    topic: str
    status: str

class ConversationMessage(BaseModel):
    message_id: str
    topic: str
    content: str
    sender_id: str

class ConversationResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    conversation_id: str
    matchflow_id: str
    current_topic: str
    topics: List[ConversationTopic]
    messages: List[ConversationMessage]
    contact_warning: str

class PostMessageRequest(BaseModel):
    topic: str
    content: str

class PostMessageResponse(BaseModel):
    message_id: Optional[str] = None
    topic: Optional[str] = None
    accepted: bool
    contact_leak_detected: bool
    message: str
