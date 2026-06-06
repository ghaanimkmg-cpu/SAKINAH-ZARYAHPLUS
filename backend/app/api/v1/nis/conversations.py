from fastapi import APIRouter, Depends, HTTPException
from app.nis.schemas.structured_conversation import ConversationResponse, PostMessageRequest, PostMessageResponse
from app.nis.services.structured_conversation_service import NISStructuredConversationService
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext

router = APIRouter()

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: str, current_user: UserContext = Depends(get_current_user)):
    try:
        return NISStructuredConversationService.get_conversation(conversation_id, current_user.user_id)
    except ValueError as e:
        if "Unauthorized" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{conversation_id}/messages", response_model=PostMessageResponse)
async def post_message(conversation_id: str, req: PostMessageRequest, current_user: UserContext = Depends(get_current_user)):
    try:
        return NISStructuredConversationService.post_message(
            conversation_id, 
            current_user.user_id, 
            req.topic, 
            req.content
        )
    except ValueError as e:
        if "Unauthorized" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
