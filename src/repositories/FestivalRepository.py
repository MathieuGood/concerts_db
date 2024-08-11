from sqlalchemy.orm import Session
from src.entities.Festival import Festival
from src.repositories.BaseRepository import BaseRepository


class FestivalRepository(BaseRepository[Festival]):
    def __init__(self, session: Session):
        super().__init__(session, Festival)