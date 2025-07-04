# backend/app/routers/reports.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import schemas, database
# COMENTE OU REMOVA ESTA LINHA:
# from ..services.gemini import generate_report 
from ..dependencies import get_current_active_user

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)
