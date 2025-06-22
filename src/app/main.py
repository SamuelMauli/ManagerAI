# src/app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import Base, engine
from .jobs.email_scheduler import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Contexto de vida da aplicação para iniciar e parar serviços de fundo.
    """
    # Cria as tabelas no banco de dados (se não existirem)
    # Em produção, é melhor usar Alembic para migrações.
    Base.metadata.create_all(bind=engine)
    
    # Inicia o agendador de jobs
    scheduler.start()
    print("Scheduler iniciado...")
    
    yield
    
    # Para o agendador de jobs quando a aplicação desliga
    scheduler.shutdown()
    print("Scheduler parado.")

app = FastAPI(
    title="Personal AI Manager",
    description="Seu assistente pessoal para e-mails, tarefas e calendário.",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint inicial para verificar se a API está funcionando."""
    return {"message": "Bem-vindo ao Personal AI Manager!"}

# Aqui adicionaremos as rotas de outros módulos depois
# from .routes import email_routes, youtrack_routes, etc.
# app.include_router(email_routes.router)