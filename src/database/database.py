from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entities.base import Base
from config import Config
from sqlalchemy.orm import Session
from mockup_data.concerts_mock_data import venues, nofx_show, nfg_show, festivals
from repositories.venue import VenueRepository
from repositories.attendee import AttendeeRepository
from repositories.festival import FestivalRepository
from repositories.show import ShowRepository
from repositories.artist import ArtistRepository


def delete_database() -> None:
    import os

    try:
        os.remove("flask_concerts_db.sqlite")
        print("*** Database file removed ***")
    except FileNotFoundError as e:
        print(e)
        pass

    print("")
    # input("Press Enter to continue...")
    print("Current diretory :")
    print(os.getcwd())
    print("")


def seed_data(session: Session) -> None:
    venue_repository = VenueRepository(session)
    show_repository = ShowRepository(session)
    attendee_repository = AttendeeRepository(session)
    festival_repository = FestivalRepository(session)
    artist_repository = ArtistRepository(session)
    venue_repository.add_multiple(venues)
    festival_repository.add_multiple(festivals)
    show_repository.add(nofx_show)
    show_repository.add(nfg_show)
    session.commit()


def get_db():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
