from sqlalchemy.orm import Session
from repositories.base import BaseRepository
from models.attendee import Attendee


class AttendeeRepository(BaseRepository[Attendee]):
    def __init__(self, session: Session):
        super().__init__(session, Attendee)
