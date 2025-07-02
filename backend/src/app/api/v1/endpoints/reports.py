from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app import schemas
from app.services.report_service import report_service

router = APIRouter()

@router.post("/tasks-by-project", response_model=schemas.ReportResponse)
async def create_tasks_by_project_report(
    *,
    db: Session = Depends(deps.get_db),
    report_in: schemas.TasksByProjectReportRequest,
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """
    Gera um relatório de tarefas para um projeto específico usando IA.
    """
    report = await report_service.generate_tasks_by_project_report(
        db=db, report_request=report_in, user_id=current_user_id
    )
    if not report:
        raise HTTPException(status_code=404, detail="Não foi possível gerar o relatório.")
    return report