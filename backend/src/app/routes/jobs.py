from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ..services import email_service, youtrack_service
from ..database import get_db

router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"],
)

@router.post("/email/run", status_code=202)
async def run_email_job(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Manually triggers the background job to fetch emails.
    """
    background_tasks.add_task(email_service.fetch_and_store_emails, db)
    return {"message": "Email fetching job has been triggered in the background."}


@router.post("/youtrack/run", status_code=202)
async def run_youtrack_job(background_tasks: BackgroundTasks):
    """
    Manually triggers the background job to sync YouTrack tasks.
    """
    background_tasks.add_task(youtrack_service.sync_youtrack_tasks)
    return {"message": "YouTrack synchronization job has been triggered in the background."}