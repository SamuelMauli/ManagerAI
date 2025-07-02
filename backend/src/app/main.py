# backend/src/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from app.routes import auth, users, tasks, emails, settings, chat, calendar, dashboard
from app.services.email_service import start_email_fetching

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando a busca de e-mails em segundo plano...")
    try:
        asyncio.create_task(start_email_fetching())
    except Exception as e:
        print(f"Não foi possível iniciar a busca de emails: {e}")
    yield
    print("Aplicação encerrada.")

app = FastAPI(lifespan=lifespan, title="ManagerAI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(emails.router, prefix="/api/emails", tags=["Emails"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["Calendar"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to ManagerAI API"}