from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.venue import get, get_all, create, update, delete
from database.database import get_db
from schemas.VenueSchema import VenueCreate

router = APIRouter()
session = Depends(get_db)

router = APIRouter()


@router.get("/venue/{venue_id}")
def get_venue(venue_id: int, db: Session = session):
    return get(db, venue_id)


@router.get("/venue/")
def get_all_venues(db: Session = session):
    return get_all(db)


# Create venue
@router.post("/venue/")
def create_venue(venue: VenueCreate, db: Session = session):
    return create(db, venue)


# Update venue
@router.put("/venue/{venue_id}")
def update_venue(venue_id: int, venue: VenueCreate, db: Session = session):
    return update(db, venue_id, venue)


# Delete venue
@router.delete("/venue/{venue_id}")
def delete_venue(venue_id: int, db: Session = session):
    return delete(db, venue_id)
