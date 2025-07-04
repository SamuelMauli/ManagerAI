# backend/app/services/ai_agent.py

from . import gemini
from .tools import AVAILABLE_TOOLS
from .. import models
from sqlalchemy.orm import Session

async def process_user_intent(prompt: str, user: models.User, db: Session):
    """
    Orquestra a conversa usando o Gemini para decisão e as ferramentas locais para execução.
    """
    print(f"Processando prompt: '{prompt}'")
    
    # 1. Envia o prompt e a lista de ferramentas para o Gemini
    gemini_response_content = await gemini.get_gemini_response_with_tools(prompt)

    if not gemini_response_content or not gemini_response_content.parts:
        return "Desculpe, não consegui processar sua solicitação no momento."

    # Verifica se o Gemini solicitou uma chamada de função
    if gemini_response_content.parts[0].function_call:
        function_call = gemini_response_content.parts[0].function_call
        tool_name = function_call.name
        tool_args = {key: value for key, value in function_call.args.items()}

        print(f"Gemini solicitou a ferramenta: '{tool_name}' com os argumentos: {tool_args}")

        # 2. Encontra a função Python correspondente no nosso catálogo
        if tool_name in AVAILABLE_TOOLS:
            tool_function = AVAILABLE_TOOLS[tool_name]
            
            # Adiciona 'user' e 'db' aos argumentos se a função precisar deles
            import inspect
            sig = inspect.signature(tool_function)
            if 'user' in sig.parameters:
                tool_args['user'] = user
            if 'db' in sig.parameters:
                tool_args['db'] = db
            
            try:
                # 3. Executa a ferramenta
                tool_result = await tool_function(**tool_args)
                
                # Formata o resultado para uma resposta amigável (pode ser melhorado)
                if isinstance(tool_result, list) and len(tool_result) > 0:
                    return "\n".join([str(item) for item in tool_result])
                elif isinstance(tool_result, list):
                    return "Não encontrei nenhum resultado."
                
                return str(tool_result)

            except Exception as e:
                print(f"!!! ERRO EXECUTANDO FERRAMENTA '{tool_name}': {e}")
                return f"Ocorreu um erro ao tentar executar a ação: {e}"
        else:
            return f"A IA tentou usar uma ferramenta desconhecida: {tool_name}"
    
    # Se o Gemini respondeu com texto, apenas retorne o texto
    else:
        return gemini_response_content.parts[0].text