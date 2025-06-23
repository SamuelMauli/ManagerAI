from pydantic import BaseModel

class DashboardStats(BaseModel):
    unread_emails: int
    pending_tasks: int
    active_projects: int