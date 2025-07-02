from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app import schemas
from app.services.dashboard_service import dashboard_service

router = APIRouter()

@router.get("/project/{project_id}", response_model=schemas.ProjectDashboardResponse)
def get_project_dashboard(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """
    Obtém dados agregados para o dashboard de um projeto específico.
    """
    dashboard_data = dashboard_service.get_project_dashboard_data(
        db=db, project_id=project_id, user_id=current_user_id
    )
    if not dashboard_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado ou sem dados.")
    return dashboard_data