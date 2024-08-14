from typing import List, Type
from sqlalchemy.orm import Session
from entities.Concert import Concert
from repositories.BaseRepository import BaseRepository
from entities.Venue import Venue


class VenueRepository(BaseRepository[Venue]):
    def __init__(self, session: Session):
        super().__init__(session, Venue)
