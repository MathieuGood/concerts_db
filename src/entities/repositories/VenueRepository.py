from typing import List, Type
from sqlalchemy.orm import Session
from entities.Venue import Venue


class VenueRepository():
    def __init__(self, session: Session):
        self.session = session

    def add(self, venue) -> None:
        self.session.add(venue)
        self.session.commit()

    def add_multiple(self, venues: List[Venue]) -> None:
        self.session.add_all(venues)
        self.session.commit()

    def get_by_id(self, id) -> Type[Venue] | None:
        return self.session.get(Venue, id)

    def get_all(self) -> List[Venue]:
        return self.session.query(Venue).all()

    def delete(self, id) -> None:
        venue = self.get_by_id(id)
        self.session.delete(venue)
        self.session.commit()
