# backend/app/main.py

from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, chat, tasks, calendar, reports, dashboard, jobs, settings

# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ManagerAI Backend",
    description="API para o ManagerAI, seu assistente pessoal com IA.",
    version="1.0.0"
)

# Inclui os roteadores da API
API_PREFIX = "/api/"
app.include_router(auth.router, prefix=f"{API_PREFIX}/auth", tags=["Auth"])
app.include_router(chat.router, prefix=f"{API_PREFIX}/chat", tags=["Chat"])
app.include_router(reports.router, prefix=f"{API_PREFIX}/reports", tags=["Reports"])
app.include_router(tasks.router, prefix=f"{API_PREFIX}/tasks", tags=["Tasks"])
app.include_router(calendar.router, prefix=f"{API_PREFIX}/calendar", tags=["Calendar"])
app.include_router(dashboard.router, prefix=f"{API_PREFIX}/dashboard", tags=["Dashboard"])
app.include_router(jobs.router, prefix=f"{API_PREFIX}/jobs", tags=["Jobs"])
app.include_router(settings.router, prefix=f"{API_PREFIX}/settings", tags=["Settings"])


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do ManagerAI"}