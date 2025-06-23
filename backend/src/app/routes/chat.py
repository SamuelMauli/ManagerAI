from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, models, services
from ..dependencies import get_db, get_current_active_user

router = APIRouter()

@router.post("/chat/message", response_model=schemas.chat.ChatMessage)
async def post_chat_message(
    message: schemas.chat.ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Receives a user message, gets a response from the AI, and saves both.
    """
    # 1. Save the user's message
    services.chat_service.create_chat_message(db, sender="user", message=message.message, user_id=current_user.id)
    
    # 2. Get AI response
    ai_response_text = await services.groq_service.get_chat_response(message.message)
    
    # 3. Save the AI's response and return it
    ai_message = services.chat_service.create_chat_message(db, sender="ai", message=ai_response_text, user_id=current_user.id)
    
    return ai_message