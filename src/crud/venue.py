from entities.Venue import Venue
from fastapi import HTTPException
from schemas.VenueSchema import VenueCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get(db: Session, venue_id: int):
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        raise HTTPException(
            status_code=404, detail=f"Venue with ID {venue_id} not found."
        )
    return venue


def get_all(db: Session):
    return db.query(Venue).all()


def create(db: Session, venue: VenueCreate) -> Venue:
    try:
        db_venue = Venue(name=venue.name)
        db.add(db_venue)
        db.commit()
        db.refresh(db_venue)
        return db_venue
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Venue '{db_venue.name}' already exists."
        )


def update(db: Session, venue_id: int, venue: VenueCreate) -> Venue:
    try:
        db_venue: Venue = (
            db.query(Venue).filter(Venue.id == venue_id).first()
        )
        if db_venue is None:
            raise HTTPException(
                status_code=404, detail=f"Venue with ID {venue_id} not found."
            )
        db_venue.name = venue.name
        db.commit()
        db.refresh(db_venue)
        return db_venue
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Venue '{venue.name}' already exists."
        )


def delete(db: Session, venue_id: int):
    db_venue: Venue = (
        db.query(Venue).filter(Venue.id == venue_id).first()
    )
    if not db_venue:
        return {"message": f"Venue #{venue_id} does not exist."}
    venue_name = db_venue.name
    db.delete(db_venue)
    db.commit()
    return {"message": f"Venue #{venue_id} '{venue_name}' deleted."}
