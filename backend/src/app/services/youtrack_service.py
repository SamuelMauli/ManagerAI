from httpx import AsyncClient, BasicAuth
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..core.security import decrypt_data

async def get_youtrack_api_client(db: Session, user_id: int):
    """
    Cria e retorna um cliente HTTPX autenticado para a API do YouTrack.
    """
    base_url = crud.setting.get_setting(db, user_id, "youtrack_base_url")
    token = crud.setting.get_setting(db, user_id, "youtrack_token")

    if not base_url or not token:
        return None

    decrypted_token = decrypt_data(token)
    headers = {
        "Authorization": f"Bearer {decrypted_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    return AsyncClient(base_url=f"{base_url}/api", headers=headers)

async def sync_youtrack_data(db: Session, user_id: int):
    """
    Função principal que orquestra a sincronização de todos os dados do YouTrack.
    """
    api = await get_youtrack_api_client(db, user_id)
    if not api:
        print(f"Skipping YouTrack sync for user {user_id}: settings not found.")
        return

    async with api:
        await _sync_projects(api, db, user_id)
        await _sync_issues(api, db, user_id)
    
    print(f"YouTrack data synchronized successfully for user {user_id}")

async def _sync_projects(api: AsyncClient, db: Session, user_id: int):
    """ Sincroniza os projetos do YouTrack. """
    fields = "id,name,shortName"
    response = await api.get(f"/admin/projects?fields={fields}")
    response.raise_for_status()
    
    for project_data in response.json():
        project_schema = schemas.project.ProjectCreate(
            external_id=project_data.get('id'),
            name=project_data.get('name'),
            short_name=project_data.get('shortName')
        )
        crud.project.create_or_update_project(db=db, project_in=project_schema, owner_id=user_id)

async def _sync_issues(api: AsyncClient, db: Session, user_id: int):
    """ Sincroniza as issues (tarefas) do YouTrack. """
    fields = (
        "id,idReadable,summary,description,"
        "created,updated,"
        "project(shortName),"
        "reporter(login,fullName),"
        "customFields(name,value(name,login,fullName))"
    )
    response = await api.get(f"/issues?fields={fields}")
    response.raise_for_status()

    for issue_data in response.json():
        project_short_name = issue_data.get('project', {}).get('shortName')
        project = crud.project.get_by_short_name(db, project_short_name, user_id)

        if not project:
            continue

        assignee_name = None
        status = None
        for field in issue_data.get('customFields', []):
            if field.get('name') == 'Assignee' and field.get('value'):
                assignee_name = field['value'].get('fullName') or field['value'].get('login')
            if field.get('name') == 'State' and field.get('value'):
                status = field['value'].get('name')

        task_schema = schemas.task.TaskCreate(
            external_id=issue_data.get('id'),
            title=issue_data.get('summary'),
            description=issue_data.get('description', ''),
            status=status,
            assignee=assignee_name,
            project_id=project.id,
            created_at=issue_data.get('created'),
            updated_at=issue_data.get('updated')
        )
        crud.task.create_or_update_task(db=db, task_in=task_schema, owner_id=user_id)