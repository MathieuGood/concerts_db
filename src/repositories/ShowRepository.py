from sqlalchemy.orm import Session
from entities.Show import Show
from repositories.BaseRepository import BaseRepository


class ShowRepository(BaseRepository[Show]):
    def __init__(self, session: Session):
        super().__init__(session, Show)