from sqlalchemy.orm import Session
from entities.festival import Festival
from repositories.base import BaseRepository


class FestivalRepository(BaseRepository[Festival]):
    def __init__(self, session: Session):
        super().__init__(session, Festival)