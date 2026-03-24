from sqlalchemy.orm import Session
from models.event import Event
from repositories.base import BaseRepository


class EventRepository(BaseRepository[Event]):
    def __init__(self, session: Session):
        super().__init__(session, Event)
