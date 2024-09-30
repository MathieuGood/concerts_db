from sqlalchemy.orm import Session
from models.concert import Concert
from repositories.base import BaseRepository


class ConcertRepository(BaseRepository[Concert]):
    def __init__(self, session: Session):
        super().__init__(session, Concert)