from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import tasks, projects, settings, jobs, dashboard, emails, chat 
from .database import Base, engine
from .routes import (
    dashboard,
    emails,
    tasks,
    chat,
    settings as settings_router,
    jobs
)
from .initial_data import create_first_superuser

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ManagerAI API",
    description="API para o sistema ManagerAI, unindo produtividade e inteligência artificial.",
    version="1.0.0"
)

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Inclusão das Rotas da API ---
app.include_router(settings_router.router, prefix="/api", tags=["Settings"])
app.include_router(dashboard.router, prefix="/api", tags=["Dashboard"])
app.include_router(emails.router, prefix="/api", tags=["Emails"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(jobs.router, prefix="/api", tags=["Jobs"])

@app.on_event("startup")
async def startup_event():
    """
    Cria o primeiro superusuário ao iniciar a aplicação, se ele não existir.
    """
    create_first_superuser()

@app.get("/")
def read_root():
    """Endpoint raiz da API."""
    return {"message": "Bem-vindo à API do ManagerAI"}