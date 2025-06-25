from pydantic import BaseModel

class DashboardStats(BaseModel):
    total_tasks: int
    total_projects: int
    unread_emails: int

    class Config:
        from_attributes = True