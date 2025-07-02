from sqlalchemy.orm import Session
from app import crud
from app.services.groq_service import GroqService

class AiService:
    def __init__(self):
        self.llm_provider = GroqService()

    async def get_contextual_chat_response(self, db: Session, user_prompt: str, user_id: int) -> str:
        # 1. Recuperação (Retrieval) - Buscar dados relevantes
        tasks = crud.task.get_multi_by_owner(db, owner_id=user_id, limit=20)
        emails = crud.email.get_multi_by_owner(db, owner_id=user_id, limit=10)
        events = crud.calendar_event.get_multi_by_owner(db, owner_id=user_id, limit=10)

        # 2. Aumento (Augmentation) - Montar o prompt com contexto
        context = "### Contexto Interno do Sistema ###\n\n"
        
        context += "Tarefas Recentes (YouTrack):\n"
        if tasks:
            for task in tasks:
                context += f"- ID: {task.youtrack_id}, Título: {task.title}, Status: {task.status}\n"
        else:
            context += "Nenhuma tarefa encontrada.\n"

        context += "\nE-mails Recentes (Gmail):\n"
        if emails:
            for email in emails:
                context += f"- De: {email.sender}, Assunto: {email.subject}, Resumo: {email.summary}\n"
        else:
            context += "Nenhum e-mail encontrado.\n"
            
        context += "\nPróximos Eventos (Google Calendar):\n"
        if events:
            for event in events:
                context += f"- Evento: {event.summary}, Início: {event.start_time.strftime('%d/%m %H:%M')}\n"
        else:
            context += "Nenhum evento encontrado.\n"

        # 3. Geração (Generation)
        system_prompt = f"""
        Você é 'ManagerAI', um assistente de gestão inteligente. Sua função é responder às perguntas do usuário de forma concisa e precisa, 
        baseando-se EXCLUSIVAMENTE no 'Contexto Interno do Sistema' fornecido abaixo. Não invente informações. Se a resposta não estiver no contexto, 
        diga que não possui a informação.

        {context}
        """

        response_text = await self.llm_provider.get_response(system_prompt, user_prompt)
        return response_text

    async def get_response(self, system_prompt: str, user_prompt: str) -> str:
        """
        Método genérico para chamadas diretas à IA, usado pelos relatórios.
        """
        return await self.llm_provider.get_response(system_prompt, user_prompt)


ai_service = AiService()