# backend/src/app/routes/chat.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, models, schemas, services
from ..core.security import get_current_active_user
from ..database import get_db

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)

@router.post("/message", response_model=schemas.chat.ChatMessage)
async def post_chat_message(
    message: schemas.chat.ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Recebe uma mensagem do usuário, obtém uma resposta do serviço de IA,
    salva ambas as mensagens e retorna a resposta da IA.
    """
    try:
        # 1. Salva a mensagem do usuário usando a camada CRUD
        crud.chat.create_chat_message(
            db=db,
            sender="user",
            message=message.message,
            user_id=current_user.id
        )

        # 2. Obtém a resposta do serviço de IA (Groq)
        ai_response_text = await services.groq_service.get_chat_response(message.message)

        # 3. Salva a resposta da IA e a retorna
        ai_message = crud.chat.create_chat_message(
            db=db,
            sender="ai",
            message=ai_response_text,
            user_id=current_user.id
        )

        return ai_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a mensagem do chat: {e}")