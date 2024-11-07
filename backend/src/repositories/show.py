from sqlalchemy.orm import Session
from models.show import Show
from repositories.base import BaseRepository


class ShowRepository(BaseRepository[Show]):
    def __init__(self, session: Session):
        super().__init__(session, Show)