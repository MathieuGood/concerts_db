from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from database.database import delete_database, seed_data
from entities.Base import Base
from config import Config
from api.routes.root import router as root_router
from api.routes.address import router as address_router
from api.routes.artist import router as artist_router
from api.routes.concert import router as concert_router
from api.routes.festival import router as festival_router
from api.routes.person import router as person_router
from api.routes.photo import router as photo_router
from api.routes.show import router as show_router
from api.routes.venue import router as venue_router
from api.routes.video import router as video_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Perform any necessary setup operations
    delete_database()
    engine: Engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db: Session = SessionLocal()
    seed_data(db)
    db.close()
    print("Data added to the database")
    print("")
    yield

    # Shutdown: Perform any necessary cleanup operations
    print("Application shutdown")


app = FastAPI()
app.include_router(root_router)
app.include_router(address_router)
app.include_router(artist_router)
app.include_router(concert_router)
app.include_router(festival_router)
app.include_router(person_router)
app.include_router(photo_router)
app.include_router(show_router)
app.include_router(venue_router)
app.include_router(video_router)

app.router.lifespan_context = lifespan
