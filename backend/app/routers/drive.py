from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user
from ..services import google as google_service

router = APIRouter(
    prefix="/drive",
    tags=["drive"],
    dependencies=[Depends(get_current_user)],
)

@router.get("/files", response_model=List[schemas.DriveFile])
def search_drive_files_endpoint(
    query: str, 
    max_results: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Busca arquivos no Google Drive do usuário pelo nome.
    """
    try:
        files = google_service.search_drive_files(current_user, query, max_results)
        return [schemas.DriveFile(
            id=file['id'],
            name=file['name'],
            mime_type=file['mime_type'],
            web_view_link=file['link'],
            created_time=datetime.datetime.fromisoformat(file['created_time'].replace('Z', '+00:00')) # Parse ISO format correctly
        ) for file in files if isinstance(files, list)] # Ensure files is a list before iterating
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/files/{file_id}/content", response_model=schemas.DriveFileContent)
def get_drive_file_content_endpoint(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Obtém o conteúdo de um arquivo específico do Google Drive.
    """
    try:
        file_content = google_service.get_drive_file_content(db, current_user, file_id)
        if not file_content:
            raise HTTPException(status_code=404, detail="File content not found or could not be retrieved.")
        return file_content
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/files", response_model=schemas.DriveFile, status_code=status.HTTP_201_CREATED)
def create_drive_file_endpoint(
    file_name: str,
    mime_type: str,
    content: str = "",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Cria um novo arquivo no Google Drive do usuário.
    """
    try:
        created_file = google_service.create_drive_file(db, current_user, file_name, mime_type, content)
        return schemas.DriveFile(
            id=created_file['id'],
            name=created_file['name'],
            mime_type=created_file['mimeType'],
            web_view_link=created_file['webViewLink'],
            created_time=datetime.datetime.fromisoformat(created_file['createdTime'].replace('Z', '+00:00'))
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))