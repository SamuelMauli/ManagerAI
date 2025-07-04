# backend/app/services/gemini.py

import google.generativeai as genai
from ..config import settings
# CORREÇÃO: Importa a variável com o nome correto
from .tools import TOOL_CONFIG 

genai.configure(api_key=settings.GOOGLE_API_KEY)

# Define o modelo com as ferramentas que ele pode usar
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    tools=TOOL_CONFIG # Passa a configuração de ferramentas no formato de dicionário
)

async def get_gemini_response_with_tools(prompt: str):
    """
    Envia o prompt para o Gemini e deixa o modelo decidir se deve
    chamar uma função ou responder diretamente.
    """
    try:
        chat = model.start_chat() 
        response = await chat.send_message_async(prompt)
        
        return response.candidates[0].content
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return None