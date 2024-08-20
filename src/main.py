from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker
from mockup_data.concerts_mock_data import venues, nofx_show, nfg_show, festivals
from database.database import delete_database, get_db
from api.routes import router
from entities.Base import Base
from entities.Person import Person
from entities.Artist import Artist
from entities.Concert import Concert
from entities.Festival import Festival
from entities.Address import Address
from entities.Venue import Venue
from repositories.VenueRepository import VenueRepository
from repositories.ConcertRepository import ConcertRepository
from repositories.PersonRepository import PersonRepository
from repositories.AddressRepository import AddressRepository
from repositories.FestivalRepository import FestivalRepository
from repositories.PhotoRepository import PhotoRepository
from repositories.VideoRepository import VideoRepository
from repositories.ShowRepository import ShowRepository


def add_data(session) -> None:
    venue_repository = VenueRepository(session)
    show_repository = ShowRepository(session)
    person_repository = PersonRepository(session)
    festival_repository = FestivalRepository(session)
    venue_repository.add_multiple(venues)
    festival_repository.add_multiple(festivals)
    show_repository.add(nofx_show)
    show_repository.add(nfg_show)
    session.commit()


app = FastAPI()
app.include_router(router)

# Launch add_data() function to add mock data to the database when the app starts
@app.on_event("startup")
def startup_event():
    engine = create_engine("sqlite:///flask_concerts_db.sqlite", echo=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    add_data(db)
    db.close()
    print("Data added to the database")
    print("")