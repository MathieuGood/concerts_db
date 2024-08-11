from sqlalchemy.orm import Session
from src.entities.Concert import Concert
from src.repositories.BaseRepository import BaseRepository


class ConcertRepository(BaseRepository[Concert]):
    def __init__(self, session: Session):
        super().__init__(session, Concert)