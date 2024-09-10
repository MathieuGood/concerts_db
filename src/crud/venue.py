from entities.Venue import Venue
from fastapi import HTTPException
from schemas.VenueSchema import VenueCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get(db: Session, venue_id: int):
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    venue.address
    if not venue:
        raise HTTPException(
            status_code=404, detail=f"Venue with ID {venue_id} not found."
        )
    return venue


def get_all(db: Session):
    venues = db.query(Venue).all()
    for venue in venues:
        venue.address
    return venues


def create(db: Session, venue: VenueCreate) -> Venue:
    try:
        new_venue = Venue(name=venue.name, address_id=venue.address_id)
        db.add(new_venue)
        db.commit()
        db.refresh(new_venue)
        return new_venue
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Venue '{new_venue.name}' already exists."
        )


def update(db: Session, venue_id: int, venue: VenueCreate) -> Venue:
    try:
        updated_venue: Venue = (
            db.query(Venue).filter(Venue.id == venue_id).first()
        )
        if updated_venue is None:
            raise HTTPException(
                status_code=404, detail=f"Venue with ID {venue_id} not found."
            )
        updated_venue.name = venue.name
        updated_venue.address_id = venue.address_id
        db.commit()
        db.refresh(updated_venue)
        return updated_venue
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Venue '{venue.name}' already exists."
        )


def delete(db: Session, venue_id: int):
    deleted_venue: Venue = (
        db.query(Venue).filter(Venue.id == venue_id).first()
    )
    if not deleted_venue:
        return {"message": f"Venue #{venue_id} does not exist."}
    db.delete(deleted_venue)
    db.commit()
    return {"message": f"Venue #{venue_id} '{deleted_venue.name}' deleted."}