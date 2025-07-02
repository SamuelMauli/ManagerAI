from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..dependencies import get_current_user


router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    # Opcional: pode adicionar a dependência para todas as rotas deste router
    # dependencies=[Depends(get_current_user)] 
)
@router.get("/")
def read_dashboard_data(
    # A dependência é injetada aqui, protegendo a rota
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Agora você tem acesso ao usuário logado através de 'current_user'
    return {"message": f"Bem-vindo ao seu dashboard, {current_user.name}!"}

@router.get("/project/{project_id}")
def get_project_dashboard_data(project_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Lógica de exemplo para buscar dados do dashboard
    tasks_query = db.query(models.Task).filter(
        models.Task.user_id == current_user.id, 
        models.Task.project_id == project_id
    )
    
    total_tasks = tasks_query.count()
    unresolved_tasks = tasks_query.filter(models.Task.status != 'Feito').count() # Exemplo
    
    task_counts_by_status = db.query(
        models.Task.status, func.count(models.Task.id)
    ).filter(
        models.Task.user_id == current_user.id,
        models.Task.project_id == project_id
    ).group_by(models.Task.status).all()

    formatted_counts = [{"status": status, "count": count} for status, count in task_counts_by_status]

    return {
        "total_tasks": total_tasks,
        "unresolved_tasks": unresolved_tasks,
        "task_counts_by_status": formatted_counts
    }