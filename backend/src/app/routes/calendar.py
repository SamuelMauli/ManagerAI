from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_calendar_events():
    return {"message": "Calendar endpoint is active"}