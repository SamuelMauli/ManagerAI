from pydantic import BaseModel
from typing import List, Dict

class TaskStatusCount(BaseModel):
    status: str
    count: int

class ProjectDashboardResponse(BaseModel):
    project_id: str
    project_name: str
    task_counts_by_status: List[TaskStatusCount]
    total_tasks: int
    unresolved_tasks: int