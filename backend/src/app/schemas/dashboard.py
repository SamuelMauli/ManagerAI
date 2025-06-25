from pydantic import BaseModel

class DashboardStats(BaseModel):
    pending_tasks: int
    new_emails: int
    total_users: int

    class Config:
        from_attributes = True