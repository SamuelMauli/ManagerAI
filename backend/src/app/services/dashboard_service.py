from sqlalchemy.orm import Session
from sqlalchemy import func
from app import crud, models, schemas

class DashboardService:
    def get_project_dashboard_data(
        self, db: Session, *, project_id: str, user_id: int
    ) -> schemas.ProjectDashboardResponse:
        project = crud.project.get_by_youtrack_id(db, youtrack_id=project_id, owner_id=user_id)
        if not project:
            return None 

        task_counts = db.query(
            models.Task.status, func.count(models.Task.id)
        ).filter(
            models.Task.project_id == project_id, 
            models.Task.owner_id == user_id
        ).group_by(models.Task.status).all()

        total_tasks = sum(count for _, count in task_counts)
        unresolved_tasks = sum(count for status, count in task_counts if status.lower() != 'resolved')

        return schemas.ProjectDashboardResponse(
            project_id=project.youtrack_id,
            project_name=project.name,
            task_counts_by_status=[schemas.TaskStatusCount(status=status, count=count) for status, count in task_counts],
            total_tasks=total_tasks,
            unresolved_tasks=unresolved_tasks,
        )

dashboard_service = DashboardService()