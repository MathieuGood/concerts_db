from entities.concert import Concert
from fastapi import HTTPException
from schemas.concert import ConcertCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get(db: Session, concert_id: int):
    concert = db.query(Concert).filter(Concert.id == concert_id).first()
    concert.artist
    concert.photos
    concert.videos
    if not concert:
        raise HTTPException(
            status_code=404, detail=f"Concert with ID {concert_id} not found."
        )
    return concert


def get_all(db: Session):
    concerts = db.query(Concert).all()
    for concert in concerts:
        concert.artist
        concert.photos
        concert.videos
    return concerts


def create(db: Session, concert: ConcertCreate) -> Concert:
    try:
        new_concert = Concert(
            comments=concert.comments,
            setlist=concert.setlist,
            show_id=concert.show_id,
            artist_id=concert.artist_id,
        )
        db.add(new_concert)
        db.commit()
        db.refresh(new_concert)
        return new_concert
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Concert '{new_concert.artist}' already exists."
        )


def update(db: Session, concert_id: int, concert: ConcertCreate) -> Concert:
    try:
        updated_concert: Concert = db.query(Concert).filter(Concert.id == concert_id).first()
        if updated_concert is None:
            raise HTTPException(
                status_code=404, detail=f"Concert with ID {concert_id} not found."
            )
        updated_concert.comments = concert.comments
        updated_concert.setlist = concert.setlist
        updated_concert.show_id = concert.show_id
        updated_concert.artist_id = concert.artist_id
        db.commit()
        db.refresh(updated_concert)
        return updated_concert
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Concert '{concert.artist}' already exists."
        )


def delete(db: Session, concert_id: int):
    deleted_concert: Concert = db.query(Concert).filter(Concert.id == concert_id).first()
    if not deleted_concert:
        return {"message": f"Concert #{concert_id} does not exist."}
    db.delete(deleted_concert)
    db.commit()
    return {"message": f"Concert #{concert_id} deleted."}
