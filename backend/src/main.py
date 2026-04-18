from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from database.database import engine
from models.base import Base

from routes.root import router as root_router
from routes.country import router as country_router
from routes.city import router as city_router
from routes.artist import router as artist_router
from routes.festival import router as festival_router
from routes.attendee import router as attendee_router
from routes.event import router as event_router
from routes.venue import router as venue_router
from routes.auth import router as auth_router
from routes.admin import router as admin_router
from routes.transfer import router as transfer_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
    print("Application shutdown")


app = FastAPI(lifespan=lifespan, root_path="/api")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "data": None, "message": exc.detail},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://concerts.mathieubon.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(root_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(transfer_router)
app.include_router(country_router)
app.include_router(city_router)
app.include_router(artist_router)
app.include_router(festival_router)
app.include_router(attendee_router)
app.include_router(event_router)
app.include_router(venue_router)
