from pydantic import BaseModel, Field
from typing import List, Dict, Any

class TasksByProjectReportRequest(BaseModel):
    project_id: str = Field(..., description="ID do projeto no YouTrack.")
    user_prompt: str = Field("Gerar um resumo do status atual do projeto, destacando tarefas críticas e atrasadas.", 
                             description="Instrução para a IA gerar o relatório.")

class ReportResponse(BaseModel):
    report_format: str = "markdown"
    data: Dict[str, Any]
    content: str