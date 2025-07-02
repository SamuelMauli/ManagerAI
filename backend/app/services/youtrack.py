import httpx
from typing import Optional, List, Dict, Any

async def get_youtrack_projects(base_url: str, token: str) -> List[Dict[str, Any]]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    # Os campos podem variar dependendo da sua versão do YouTrack
    fields = "id,name,shortName"
    url = f"{base_url}/api/admin/projects?fields={fields}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

async def get_youtrack_tasks(base_url: str, token: str, project_id: str) -> List[Dict[str, Any]]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    # Campos customizados podem precisar ser adicionados
    fields = "id,summary,description,project(id,name),customFields(name,value(name,login))"
    query = f"project: {project_id}"
    url = f"{base_url}/api/issues?fields={fields}&query={query}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred while fetching tasks: {e.response.status_code} - {e.response.text}")
            return []
        except Exception as e:
            print(f"An error occurred while fetching tasks: {e}")
            return []