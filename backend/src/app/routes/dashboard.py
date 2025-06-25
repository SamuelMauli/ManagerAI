from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..services import google_service, youtrack_service, groq_service
from .. import models, schemas

from .. import crud, models, schemas
from ..core.security import get_current_active_user
from ..database import get_db

router = APIRouter()

@router.get("/dashboard/stats", response_model=schemas.dashboard.DashboardStats)
async def get_dashboard_stats(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Fetches statistics for the dashboard: unread emails, pending tasks, and active projects.
    """
    # Gmail Unread Count
    gmail_service = google_service.get_gmail_service(current_user.id)
    email_results = gmail_service.users().messages().list(userId='me', q="is:unread").execute()
    unread_emails_count = email_results.get('resultSizeEstimate', 0)

    # YouTrack Stats
    yt_service = youtrack_service.get_youtrack_service(db, current_user.id)
    pending_tasks_count = 0
    active_projects_count = 0
    if yt_service:
        pending_tasks_count = await yt_service.get_pending_tasks_count() 
        active_projects_count = await yt_service.get_active_projects_count()

    return {
        "unread_emails": unread_emails_count,
        "pending_tasks": pending_tasks_count,
        "active_projects": active_projects_count
    }

@router.get("/dashboard/summarized-emails", response_model=list[schemas.email.EmailSummary])
async def get_summarized_emails(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Fetches the latest summarized unread emails from the database.
    """
    emails = db.query(models.Email).filter(models.Email.owner_id == current_user.id, models.Email.is_read == False).order_by(models.Email.date.desc()).limit(5).all()
    return emails