from sqlalchemy.orm import Session
from entities.Concert import Concert
from repositories.BaseRepository import BaseRepository


class ConcertRepository(BaseRepository[Concert]):
    def __init__(self, session: Session):
        super().__init__(session, Concert)