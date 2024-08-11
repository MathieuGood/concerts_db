from sqlalchemy.orm import Session
from src.entities.Show import Show
from src.repositories.BaseRepository import BaseRepository


class ShowRepository(BaseRepository[Show]):
    def __init__(self, session: Session):
        super().__init__(session, Show)