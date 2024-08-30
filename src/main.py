from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker
from mockup_data.concerts_mock_data import venues, nofx_show, nfg_show, festivals
from database.database import delete_database, get_db
from api.routes.root import router as root_router
from api.routes.festival import router as festival_router
from api.routes.artist import router as artist_router
from api.routes.address import router as address_router
from entities.Base import Base
from repositories.VenueRepository import VenueRepository
from repositories.ConcertRepository import ConcertRepository
from repositories.PersonRepository import PersonRepository
from repositories.AddressRepository import AddressRepository
from repositories.FestivalRepository import FestivalRepository
from repositories.PhotoRepository import PhotoRepository
from repositories.VideoRepository import VideoRepository
from repositories.ShowRepository import ShowRepository
from config import Config


def add_data(session: Session) -> None:
    venue_repository = VenueRepository(session)
    show_repository = ShowRepository(session)
    person_repository = PersonRepository(session)
    festival_repository = FestivalRepository(session)
    venue_repository.add_multiple(venues)
    festival_repository.add_multiple(festivals)
    show_repository.add(nofx_show)
    show_repository.add(nfg_show)
    session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Perform any necessary setup operations
    delete_database()
    engine: Engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db: Session = SessionLocal()
    add_data(db)
    db.close()
    print("Data added to the database")
    print("")
    yield

    # Shutdown: Perform any necessary cleanup operations
    print("Application shutdown") 


app = FastAPI()
app.include_router(root_router)
app.include_router(festival_router)
app.include_router(artist_router)
app.include_router(address_router)
app.router.lifespan_context = lifespan
