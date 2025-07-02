import os
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware

# Importações que faltavam
from .database import engine, Base
from . import models # Garante que os modelos sejam "conhecidos" pelo Base do SQLAlchemy

from .routers import auth, chat, tasks, calendar, reports, dashboard, jobs, settings

# Cria as tabelas no banco de dados (se não existirem)
# Esta linha agora funcionará pois Base e engine foram importados
Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

# Inclusão dos roteadores
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(settings.router, prefix="/settings", tags=["settings"])