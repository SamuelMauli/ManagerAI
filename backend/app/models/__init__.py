from .user import User
from .email import Email
from .setting import Setting
from .task import Task
from .calendar_event import CalendarEvent

# Garanta que a Base de todos os modelos seja reconhecida
from ..database import Base