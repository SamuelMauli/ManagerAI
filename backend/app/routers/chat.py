# backend/app/routers/chat.py
from fastapi import APIRouter, Depends, HTTPException
from .. import schemas, models
from ..dependencies import get_current_user
from ..services import generative_ai

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    dependencies=[Depends(get_current_user)],
)

class ChatRequest(schemas.BaseModel):
    message: str

@router.post("/", response_model=schemas.ChatMessage)
def post_chat_message(
    request: ChatRequest,
    current_user: models.User = Depends(get_current_user)
):
    """
    Recebe uma mensagem do usuário e retorna a resposta do chatbot.
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")

    response_text = generative_ai.generate_chat_response(query=request.message, user=current_user)

    return schemas.ChatMessage(role="ai", content=response_text)