# backend/app/routers/chat.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, crud
from ..database import get_db
from ..services import ai_agent
from ..dependencies import get_current_active_user

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/", response_model=schemas.ChatMessage)
async def handle_chat_message(
    chat_request: schemas.ChatRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Endpoint central para processar mensagens do chat.
    Agora, ele sabe qual usuário está fazendo a pergunta.
    """
    try:
        # A mensagem e o usuário são enviados para o "cérebro" da IA
        response_content = await ai_agent.process_user_intent(
            prompt=chat_request.message,
            user=current_user,
            db=db
        )
        return schemas.ChatMessage(role="ai", content=response_content)
    except Exception as e:
        print(f"Erro no processamento do chat: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro ao processar sua mensagem.")