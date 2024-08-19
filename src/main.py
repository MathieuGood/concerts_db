from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker
from mockup_data.concerts_mock_data import venues, nofx_show, nfg_show, festivals
from database.database import delete_database, get_db
from schemas.AddressSchema import AddressResponse
from schemas.ShowSchema import ShowResponse
from schemas.VenueSchema import VenueResponse
from api import crud
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
from schemas.VenueSchema import VenueCreate


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

    print(venue_repository.get_all())


# Set the lifespan for the application
app = FastAPI()


@app.get("/")
def read_root():
    # venues = venue_repository.get_by_id(1)
    # Return the venues as a JSON response
    venues = "Hello World"
    return {"venues": venues}


@app.post("/venues/", response_model=VenueResponse)
def create_venue(venue: VenueCreate, db: Session = Depends(get_db)):
    return crud.create_venue(db=db, venue=venue)


@app.get("/venues/", response_model=list[VenueResponse])
def read_venues(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_venues(db=db, skip=skip, limit=limit)


@app.get("/addresses/", response_model=list[AddressResponse])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db, skip=skip, limit=limit)
    return addresses


# Route to get all festivals (shows)
@app.get("/festivals/", response_model=list[ShowResponse])
def read_festivals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    festivals = crud.get_shows(db, skip=skip, limit=limit)
    return festivals


# if __name__ == "__main__":
# main()
