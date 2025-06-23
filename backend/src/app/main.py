from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine
from .models import base
from .jobs.email_scheduler import scheduler
from .routes import settings, jobs, dashboard, emails

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context to start and stop background services.
    """
    # Create database tables if they don't exist
    base.Base.metadata.create_all(bind=engine)
    
    # Start the job scheduler
    scheduler.start()
    print("Scheduler started...")
    
    yield
    
    # Stop the job scheduler on application shutdown
    scheduler.shutdown()
    print("Scheduler stopped.")

app = FastAPI(
    title="ManagerAI Backend",
    description="Your personal assistant for emails, tasks, and more.",
    version="1.0.0",
    lifespan=lifespan
)

# Include all the new API routers
app.include_router(settings.router)
app.include_router(jobs.router)
app.include_router(dashboard.router)
app.include_router(emails.router)


@app.get("/api", tags=["Root"])
def read_root():
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to the ManagerAI Backend!"}