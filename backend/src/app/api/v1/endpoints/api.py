from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth, 
    users, 
    youtrack, 
    google, 
    chat,
    # Adicionar estas importações
    jobs,
    reports,
    dashboard
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(youtrack.router, prefix="/youtrack", tags=["youtrack"])
api_router.include_router(google.router, prefix="/google", tags=["google"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

# Adicionar estas linhas
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])