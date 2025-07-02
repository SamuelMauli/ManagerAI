from sqlalchemy.orm import Session
from app import crud, schemas
from .ai_service import ai_service
import json

class ReportService:
    async def generate_tasks_by_project_report(
        self, 
        db: Session, 
        *, 
        report_request: schemas.ReportRequest, 
        user_id: int
    ) -> schemas.ReportResponse:
        project_id = report_request.project_id
        
        tasks = crud.task.get_tasks_by_project_id(db, project_id=project_id, owner_id=user_id)
        if not tasks:
            return schemas.ReportResponse(
                data={"project_id": project_id, "task_count": 0},
                content="Nenhuma tarefa encontrada para este projeto."
            )

        tasks_data = [schemas.Task.from_orm(t).model_dump_json() for t in tasks]
        
        system_prompt = f"""
        Você é um analista de projetos sênior. Sua tarefa é analisar os dados de tarefas de um projeto, fornecidos em formato JSON, 
        e gerar um relatório em markdown que responda à solicitação do usuário.
        
        Dados das Tarefas (JSON):
        {json.dumps(tasks_data, indent=2)}
        """

        report_content = await ai_service.get_response(
            system_prompt=system_prompt,
            user_prompt=report_request.user_prompt
        )
        
        return schemas.ReportResponse(
            data={"project_id": project_id, "task_count": len(tasks)},
            content=report_content
        )

report_service = ReportService()