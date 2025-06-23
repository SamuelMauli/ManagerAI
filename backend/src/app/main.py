from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import auth, users
from .routes import dashboard, emails, tasks, chat, settings, jobs
from .core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(dashboard.router, prefix="/api", tags=["Dashboard"])
app.include_router(emails.router, prefix="/api", tags=["Emails"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(settings.router, prefix="/api", tags=["Settings"])
app.include_router(jobs.router, prefix="/api", tags=["Jobs"])


@app.get("/api")
def read_root():
    return {"message": "Welcome to ManagerAI!"}

