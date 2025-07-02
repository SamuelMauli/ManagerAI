# backend/app/routers/chat.py

from fastapi import APIRouter, Depends
from ..services.gemini import get_chat_response
from ..utils.security import get_current_user
from .. import models

# Adicione o prefixo e tags aqui
router = APIRouter(
    prefix="/chat", # Adicione esta linha
    tags=["chat"]   # Adicione esta linha (opcional, mas recomendado)
)

@router.post("", response_model=str) # O caminho pode permanecer vazio aqui, pois o prefixo já define "/chat"
def post_chat_message(message_container: dict, current_user: models.User = Depends(get_current_user)):
    message = message_container.get("message")
    # Opcional: Adicionar contexto do usuário ou da conversa
    # prompt = f"User {current_user.email} asks: {message}"
    response = get_chat_response(message)
    return response