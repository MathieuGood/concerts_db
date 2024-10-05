from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.address import Address
from models.artist import Artist
from models.attendee import Attendee
from models.base import Base
from config import Config
from sqlalchemy.orm import Session
from mockup_data.concerts_mock_data import (
    venues,
    nofx_show,
    nfg_show,
    other_festivals,
    other_addresses,
    other_artists,
    other_attendees,
)
from repositories.address import AddressRepository
from repositories.venue import VenueRepository
from repositories.attendee import AttendeeRepository
from repositories.festival import FestivalRepository
from repositories.show import ShowRepository
from repositories.artist import ArtistRepository


engine = create_engine(Config.DATABASE_URI, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    # Base.metadata.create_all(engine)
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def drop_and_recreate_all_tables(engine: create_engine) -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)
    print("\033[93mAll tables dropped and recreated\033[0m")


def seed_data(session: Session) -> None:
    venue_repository = VenueRepository(session)
    show_repository = ShowRepository(session)
    attendee_repository = AttendeeRepository(session)
    festival_repository = FestivalRepository(session)
    artist_repository = ArtistRepository(session)
    address_repository = AddressRepository(session)
    venue_repository.add_multiple(venues)
    festival_repository.add_multiple(other_festivals)
    show_repository.add(nofx_show)
    show_repository.add(nfg_show)
    address_repository.add_multiple(other_addresses)
    attendee_repository.add_multiple(other_attendees)
    artist_repository.add_multiple(other_artists)
    session.commit()
    print("\033[93mData seeded to database\033[0m")
