from entities.Concert import Concert
from fastapi import HTTPException
from schemas.ConcertSchema import ConcertCreate
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
        db_concert = Concert(
            comments=concert.comments,
            setlist=concert.setlist,
            show_id=concert.show_id,
            artist_id=concert.artist_id,
        )
        db.add(db_concert)
        db.commit()
        db.refresh(db_concert)
        return db_concert
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Concert '{db_concert.artist}' already exists."
        )


def update(db: Session, concert_id: int, concert: ConcertCreate) -> Concert:
    try:
        db_concert: Concert = db.query(Concert).filter(Concert.id == concert_id).first()
        if db_concert is None:
            raise HTTPException(
                status_code=404, detail=f"Concert with ID {concert_id} not found."
            )
        db_concert.comments = concert.comments
        db_concert.setlist = concert.setlist
        db_concert.show_id = concert.show_id
        db_concert.artist_id = concert.artist_id
        db.commit()
        db.refresh(db_concert)
        return db_concert
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Concert '{concert.artist}' already exists."
        )


def delete(db: Session, concert_id: int):
    db_concert: Concert = db.query(Concert).filter(Concert.id == concert_id).first()
    if not db_concert:
        return {"message": f"Concert #{concert_id} does not exist."}
    db.delete(db_concert)
    db.commit()
    return {"message": f"Concert #{concert_id} deleted."}
