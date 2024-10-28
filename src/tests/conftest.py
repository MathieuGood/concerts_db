from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from config import Config
from database.database import get_db
from models.artist import Artist
from models.attendee import Attendee
from models.base import Base
from models.address import Address
from models.concert import Concert
from models.festival import Festival
from models.show import Show
from models.venue import Venue

# from src.database.database import get_db
# from src.models.base import Base

print("Loading conftest.py")


@pytest.fixture(scope="function")
def client():
    engine = create_engine(
        Config.TEST_DATABASE_URI,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            seed_data(db)
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    # Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def seed_data(session):

    address = Address(city="Los Angeles", country="USA")
    session.add(address)

    artist = Artist(name="Rage Against The Machine", address=address)
    session.add(artist)

    festival = Festival(name="Rock Am See")
    session.add(festival)

    venue = Venue(name="Konstanz", address=address)
    session.add(venue)

    attendee = Attendee(firstname="John", lastname="Cleese")
    session.add(attendee)

    show = Show(
        name="Rock Am Ring Day 1",
        event_date=datetime(year=2008, month=6, day=6),
        comments="Amazing festival, first time I saw Incubus live!",
        venue=venue,
        festival=festival,
        attendees=[attendee],
    )
    session.add(show)

    concert = Concert(
        comments="Best concert ever!",
        setlist="Pardon Me, Stellar, Drive, Wish You Were Here, Megalomaniac, Talk Shows on Mute, Nice to Know You, Warning, Sick Sad Little World, Anna Molly, Love Hurts, Adolescents, Dig, Are You In?, A Crow",
        artist=artist,
    )
    show.concerts.append(concert)
    session.add(concert)

    session.commit()
    session.close()
