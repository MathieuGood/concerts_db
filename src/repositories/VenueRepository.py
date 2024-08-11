from typing import List, Type
from sqlalchemy.orm import Session
from src.entities.Concert import Concert
from src.repositories.BaseRepository import BaseRepository
from src.entities.Venue import Venue


class VenueRepository(BaseRepository[Venue]):
    def __init__(self, session: Session):
        super().__init__(session, Venue)
