from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import os

from . import crud, models, schemas
from .database import SessionLocal, engine
from .dependencies import get_db, get_current_user, authenticate_user, create_access_token, verify_token

# Altere a importação do roteador 'settings' para 'settings_router'
from .routers import auth, calendar, dashboard, chat, tasks, reports, jobs, emails, settings as settings_router
from .config import settings # Esta linha importa o objeto de configuração, que permanece com o nome 'settings'

# Cria todas as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuração CORS (se necessário para o seu ambiente de desenvolvimento/produção)
origins = [
    "http://localhost:5173",  # Frontend local
    "http://127.0.0.1:5173",  # Frontend local
    os.getenv("FRONTEND_URL", "*") # URL do frontend em produção
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Inclui os roteadores
app.include_router(auth.router)
app.include_router(calendar.router)
app.include_router(dashboard.router)
app.include_router(chat.router)
app.include_router(tasks.router)
app.include_router(reports.router)
# Use o nome renomeado para incluir o roteador de configurações
app.include_router(settings_router.router) # Altere esta linha
app.include_router(jobs.router)
app.include_router(emails.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do ManagerAI!"}