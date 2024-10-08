from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.venue import get, get_all, create, update, delete
from database.database import get_db
from schemas.venue import VenueCreate

router = APIRouter()


@router.get("/venue/{venue_id}")
async def get_venue(venue_id: int, db: Session = Depends(get_db)):
    return get(db, venue_id)


@router.get("/venue/")
async def get_all_venues(db: Session = Depends(get_db)):
    return get_all(db)


# Create venue
@router.post("/venue/")
async def create_venue(venue: VenueCreate, db: Session = Depends(get_db)):
    return create(db, venue)


# Update venue
@router.put("/venue/{venue_id}")
async def update_venue(
    venue_id: int, venue: VenueCreate, db: Session = Depends(get_db)
):
    return update(db, venue_id, venue)


# Delete venue
@router.delete("/venue/{venue_id}")
async def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    return delete(db, venue_id)
