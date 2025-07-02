# backend/app/routers/reports.py

from fastapi import APIRouter, Depends
from ..schemas import ReportRequest, ReportResponse
from ..services.gemini import generate_report
from ..utils.security import get_current_user
from .. import models

router = APIRouter()

@router.post("/tasks-by-project", response_model=ReportResponse)
def generate_tasks_by_project_report(request: ReportRequest, current_user: models.User = Depends(get_current_user)):
    # Em um cenário real, você buscaria os dados do projeto no banco de dados
    # e os passaria como contexto para a IA.
    # Ex: tasks = crud.get_tasks_by_project(db, project_id=request.project_id)
    # context = f"Dados das tarefas: {tasks}"
    
    prompt = f"Contexto do Projeto ID {request.project_id}:\n\n{request.user_prompt}\n\nGere um relatório conciso e informativo."
    
    report_content = generate_report(prompt)
    return {"content": report_content}