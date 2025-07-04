# backend/app/routers/youtrack.py

from fastapi import APIRouter, HTTPException
from typing import List, Optional
import httpx
from ..services import youtrack as youtrack_service
from .. import schemas

router = APIRouter(
    prefix="/youtrack",
    tags=["YouTrack"]
)

# --- ROTAS DE LEITURA ---

@router.get("/projects", response_model=List[schemas.YoutrackProject], summary="Listar todos os projetos")
async def read_projects():
    try:
        return await youtrack_service.get_projects()
    except Exception as e:
        print(f"!!! ERRO AO BUSCAR PROJETOS: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar projetos.")

@router.get("/projects/{project_id}/boards", response_model=List[schemas.YoutrackBoard], summary="Listar boards de um projeto")
async def read_project_boards(project_id: str):
    try:
        return await youtrack_service.get_boards_for_project(project_id)
    except Exception as e:
        print(f"!!! ERRO AO BUSCAR BOARDS: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar boards.")

# ## ROTA CORRIGIDA ##
# Esta rota agora corresponde exatamente ao que o frontend chama.
@router.get("/issues/{project_short_name}", response_model=List[schemas.YoutrackIssue], summary="Listar issues de um projeto/board")
async def read_issues(project_short_name: str, board_name: Optional[str] = None):
    try:
        return await youtrack_service.get_issues(project_short_name, board_name)
    except httpx.HTTPStatusError as e:
        print(f"!!! ERRO DE API YOUTRACK (Issues): {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
    except Exception as e:
        print(f"!!! ERRO INESPERADO (Issues): {e}")
        raise HTTPException(status_code=500, detail="Erro inesperado ao buscar issues.")

# --- ROTAS ADICIONAIS PARA O FUTURO ---

@router.get("/issue/{issue_id}", response_model=schemas.YoutrackIssue, summary="Buscar um issue por ID")
async def read_single_issue(issue_id: str):
    try:
        return await youtrack_service.get_issue_by_id(issue_id)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())

@router.post("/issue", response_model=schemas.YoutrackIssue, summary="Criar um novo issue")
async def create_issue(project_id: str, summary: str, description: Optional[str] = None):
    try:
        return await youtrack_service.create_issue(project_id, summary, description)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())

@router.put("/issue/{issue_id}", response_model=schemas.YoutrackIssue, summary="Atualizar um issue")
async def update_issue(issue_id: str, summary: str):
    try:
        return await youtrack_service.update_issue_summary(issue_id, summary)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())