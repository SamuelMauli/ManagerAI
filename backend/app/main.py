# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from . import models
from .database import engine
# Supondo que seus routers estejam em app.routers
from .routers import auth, calendar, dashboard, chat, tasks, reports, emails, settings as settings_router

# Esta linha cria as tabelas no banco de dados se elas não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    os.getenv("FRONTEND_URL", "*")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclua seus routers aqui
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(calendar.router)
app.include_router(chat.router)
app.include_router(tasks.router)
app.include_router(reports.router)
app.include_router(settings_router.router)
app.include_router(emails.router)


@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do ManagerAI!"}