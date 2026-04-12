from models.artist import Artist
from models.concert import Concert
from fastapi import HTTPException
from models.event import Event
from schemas.concert import ConcertCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload


def get(db: Session, concert_id: int):
    concert = (
        db.query(Concert)
        .options(
            joinedload(Concert.artist),
            joinedload(Concert.photos),
            joinedload(Concert.videos),
        )
        .filter(Concert.id == concert_id)
        .first()
    )
    if not concert:
        raise HTTPException(
            status_code=404, detail=f"Concert with ID {concert_id} not found."
        )
    return concert


def get_all(db: Session):
    concerts = (
        db.query(Concert)
        .options(
            joinedload(Concert.artist),
            joinedload(Concert.photos),
            joinedload(Concert.videos),
        )
        .all()
    )
    return concerts


def create(db: Session, concert: ConcertCreate) -> Concert:
    try:
        event: Event | None = db.query(Event).filter(Event.id == concert.event_id).first()
        if not event:
            raise HTTPException(
                status_code=404, detail=f"Event with ID {concert.event_id} not found."
            )

        artist = db.query(Artist).filter(Artist.id == concert.artist_id).first()
        if not artist:
            raise HTTPException(
                status_code=404, detail=f"Artist with ID {concert.artist_id} not found."
            )

        new_concert = Concert(
            comments=concert.comments,
            setlist=concert.setlist,
            event_id=concert.event_id,
            artist_id=concert.artist_id,
        )
        # TODO : Add check for existing event_id and artist_id
        db.add(new_concert)
        db.commit()
        db.refresh(new_concert)
        return new_concert
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="This artist is already listed for this event."
        )


def update(db: Session, concert_id: int, concert: ConcertCreate) -> Concert:
    try:
        updated_concert: Concert = (
            db.query(Concert).filter(Concert.id == concert_id).first()
        )
        if updated_concert is None:
            raise HTTPException(
                status_code=404, detail=f"Concert with ID {concert_id} not found."
            )
        updated_concert.comments = concert.comments
        updated_concert.setlist = concert.setlist
        updated_concert.event_id = concert.event_id
        updated_concert.artist_id = concert.artist_id
        db.commit()
        db.refresh(updated_concert)
        return updated_concert
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="This artist is already listed for this event."
        )


def delete(db: Session, concert_id: int):
    deleted_concert: Concert = (
        db.query(Concert).filter(Concert.id == concert_id).first()
    )
    if not deleted_concert:
        return {"message": f"Concert #{concert_id} does not exist."}
    db.delete(deleted_concert)
    db.commit()
    return {"message": f"Concert #{concert_id} deleted."}
