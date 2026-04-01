from models.venue import Venue
from models.city import City
from fastapi import HTTPException
from schemas.venue import VenueCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload


def get(db: Session, venue_id: int):
    venue = (
        db.query(Venue)
        .options(joinedload(Venue.city).joinedload(City.country))
        .filter(Venue.id == venue_id)
        .first()
    )
    if not venue:
        raise HTTPException(status_code=404, detail=f"Venue with ID {venue_id} not found.")
    return venue


def get_all(db: Session):
    return db.query(Venue).options(joinedload(Venue.city).joinedload(City.country)).all()


def create(db: Session, venue: VenueCreate) -> Venue:
    try:
        new_venue = Venue(name=venue.name, city_id=venue.city_id)
        db.add(new_venue)
        db.commit()
        return get(db, new_venue.id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Venue '{venue.name}' already exists in this city."
        )


def update(db: Session, venue_id: int, venue: VenueCreate) -> Venue:
    try:
        updated_venue = db.query(Venue).filter(Venue.id == venue_id).first()
        if updated_venue is None:
            raise HTTPException(status_code=404, detail=f"Venue with ID {venue_id} not found.")
        updated_venue.name = venue.name
        updated_venue.city_id = venue.city_id
        db.commit()
        return get(db, venue_id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Venue '{venue.name}' already exists in this city."
        )


def delete(db: Session, venue_id: int):
    deleted_venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not deleted_venue:
        return {"message": f"Venue #{venue_id} does not exist."}
    if deleted_venue.events:
        raise HTTPException(
            status_code=400,
            detail=f"Venue '{deleted_venue.name}' cannot be deleted because it has events associated with it.",
        )
    try:
        db.delete(deleted_venue)
        db.commit()
        return {"message": f"Venue #{venue_id} '{deleted_venue.name}' deleted."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Venue '{deleted_venue.name}' could not be deleted."
        )
