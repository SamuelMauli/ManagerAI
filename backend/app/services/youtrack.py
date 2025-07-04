# backend/app/services/youtrack.py

import httpx
from ..config import settings
from typing import List, Dict, Any, Optional

BASE_URL = settings.YOU_TRACK_BASE_URL.rstrip('/')
TOKEN = settings.YOU_TRACK_TOKEN
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}

# --- FUNÇÕES DE LEITURA (GET) ---

async def get_projects() -> List[Dict[str, Any]]:
    """Busca todos os projetos do YouTrack."""
    api_url = f"{BASE_URL}/api/admin/projects"
    params = {"fields": "id,name,shortName"}
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()

async def get_boards_for_project(project_id: str) -> List[Dict[str, Any]]:
    """Busca todos os agile boards de um projeto."""
    api_url = f"{BASE_URL}/api/agiles"
    params = {"fields": "id,name,projects(id)"}
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=HEADERS, params=params)
        response.raise_for_status()
        all_boards = response.json()
        return [
            b for b in all_boards
            if b.get("projects") and any(p.get("id") == project_id for p in b["projects"])
        ]

async def get_issues(project_short_name: str, board_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """Busca issues de um projeto, com filtro opcional por board."""
    api_url = f"{BASE_URL}/api/issues"
    query = f"project: {project_short_name}"
    if board_name:
        query += f' board "{board_name}"'
    
    params = {
        "query": query,
        "fields": "id,idReadable,summary,customFields(name,value(name,minutes,login))"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()

async def get_issue_by_id(issue_id: str) -> Dict[str, Any]:
    """Busca um único issue pelo seu ID (ex: PROJ-123)."""
    api_url = f"{BASE_URL}/api/issues/{issue_id}"
    params = { "fields": "id,idReadable,summary,description,customFields(name,value(name,minutes,login))" }
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()

# --- FUNÇÕES DE ESCRITA (POST, PUT) ---

async def create_issue(project_id: str, summary: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Cria um novo issue em um projeto."""
    api_url = f"{BASE_URL}/api/issues"
    issue_data = {
        "project": {"id": project_id},
        "summary": summary,
        "description": description or ""
    }
    params = { "fields": "id,idReadable,summary" }
    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, headers=HEADERS, json=issue_data, params=params)
        response.raise_for_status()
        return response.json()

async def update_issue_summary(issue_id: str, summary: str) -> Dict[str, Any]:
    """Atualiza o resumo de um issue existente."""
    api_url = f"{BASE_URL}/api/issues/{issue_id}"
    params = { "fields": "id,idReadable,summary" }
    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, headers=HEADERS, json={"summary": summary}, params=params)
        response.raise_for_status()
        return response.json()