from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session, sessionmaker
from database.database import drop_and_recreate_all_tables, seed_data
from config import Config

from routes.root import router as root_router
from routes.address import router as address_router
from routes.artist import router as artist_router
from routes.concert import router as concert_router
from routes.festival import router as festival_router
from routes.attendee import router as attendee_router
from routes.photo import router as photo_router
from routes.event import router as event_router
from routes.venue import router as venue_router
from routes.video import router as video_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from database.database import engine, Base
    if Config.DEMO_MODE:
        print("Running in demo mode")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db: Session = SessionLocal()
        drop_and_recreate_all_tables(engine=engine)
        seed_data(db)
        db.close()
    else:
        Base.metadata.create_all(engine)

    yield
    print("Application shutdown")


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(root_router)
app.include_router(address_router)
app.include_router(artist_router)
app.include_router(concert_router)
app.include_router(festival_router)
app.include_router(attendee_router)
app.include_router(photo_router)
app.include_router(event_router)
app.include_router(venue_router)
app.include_router(video_router)
