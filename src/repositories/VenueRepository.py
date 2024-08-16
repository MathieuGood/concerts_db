from typing import List, Type
from sqlalchemy.orm import Session
from entities.Concert import Concert
from repositories.BaseRepository import BaseRepository
from entities.Venue import Venue


class VenueRepository(BaseRepository[Venue]):
    def __init__(self, session: Session):
        super().__init__(session, Venue)

    def get_all(self) -> List[Venue]:
        venues = self.session.query(Venue).all()
        return sorted(
            venues,
            key=lambda venue: (venue.address.country, venue.address.city, venue.name),
        )
