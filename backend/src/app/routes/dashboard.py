from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.dashboard import DashboardStats
from ..models.email import Email
from ..database import get_db

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get statistics for the dashboard.
    """
    unread_emails_count = db.query(Email).filter(Email.processed_at == None).count()
    
    # Placeholders for tasks and projects
    pending_tasks_count = 0  # Replace with actual query on Task model
    active_projects_count = 0 # Replace with actual query on Project model
    
    return {
        "unread_emails": unread_emails_count,
        "pending_tasks": pending_tasks_count,
        "active_projects": active_projects_count,
    }