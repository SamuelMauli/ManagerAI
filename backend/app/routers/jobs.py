# backend/app/routers/jobs.py

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..utils.security import get_current_user
from ..services import google, youtrack

router = APIRouter()

@router.post("/youtrack/sync")
async def run_youtrack_sync_job(background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # background_tasks.add_task(youtrack.full_sync_logic, db, current_user)
    return {"message": "YouTrack sync job started in the background."}

@router.post("/email/sync")
async def run_email_sync_job(background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    background_tasks.add_task(google.sync_google_emails, db, current_user)
    return {"message": "Email sync job started in the background."}

@router.post("/calendar/sync")
async def run_calendar_sync_job(background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    background_tasks.add_task(google.sync_google_calendar, db, current_user)
    return {"message": "Calendar sync job started in the background."}