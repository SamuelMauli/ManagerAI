import datetime as dt
from sqlalchemy.orm import Session
from app import crud, schemas
from .google_service import get_google_api_service

class CalendarService:
    def sync_user_calendar(self, db: Session, *, user_id: int) -> dict:
        service = get_google_api_service(user_id=user_id, service_name='calendar', version='v3')

        now = dt.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=now,
            maxResults=50, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        items = events_result.get('items', [])
        
        created_count = 0
        updated_count = 0

        for item in items:
            event_id = item.get('id')
            if not event_id:
                continue

            start = item['start'].get('dateTime', item['start'].get('date'))
            end = item['end'].get('dateTime', item['end'].get('date'))

            event_schema = schemas.CalendarEventCreate(
                google_event_id=event_id,
                summary=item.get('summary', 'Sem Título'),
                description=item.get('description'),
                start_time=start,
                end_time=end,
                location=item.get('location'),
                html_link=item.get('htmlLink'),
                creator_email=item.get('creator', {}).get('email'),
                organizer_email=item.get('organizer', {}).get('email')
            )
            
            db_event = crud.calendar_event.get_by_google_event_id(db, google_event_id=event_id)
            if db_event:
                crud.calendar_event.update(db, db_obj=db_event, obj_in=event_schema)
                updated_count += 1
            else:
                crud.calendar_event.create(db, obj_in=event_schema, owner_id=user_id)
                created_count += 1

        return {"status": "success", "created": created_count, "updated": updated_count}

calendar_service = CalendarService()