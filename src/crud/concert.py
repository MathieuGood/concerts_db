from entities.Concert import Concert
from fastapi import HTTPException
from schemas.ConcertSchema import ConcertCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get(db: Session, concert_id: int):
    concert = db.query(Concert).filter(Concert.id == concert_id).first()
    if not concert:
        raise HTTPException(
            status_code=404, detail=f"Concert with ID {concert_id} not found."
        )
    return concert


def get_all(db: Session):
    return db.query(Concert).all()


def create(db: Session, concert: ConcertCreate) -> Concert:
    try:
        db_concert = Concert(name=concert.name)
        db.add(db_concert)
        db.commit()
        db.refresh(db_concert)
        return db_concert
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Concert '{db_concert.name}' already exists."
        )


def update(db: Session, concert_id: int, concert: ConcertCreate) -> Concert:
    try:
        db_concert: Concert = (
            db.query(Concert).filter(Concert.id == concert_id).first()
        )
        if db_concert is None:
            raise HTTPException(
                status_code=404, detail=f"Concert with ID {concert_id} not found."
            )
        db_concert.name = concert.name
        db.commit()
        db.refresh(db_concert)
        return db_concert
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Concert '{concert.name}' already exists."
        )


def delete(db: Session, concert_id: int):
    db_concert: Concert = (
        db.query(Concert).filter(Concert.id == concert_id).first()
    )
    if not db_concert:
        return {"message": f"Concert #{concert_id} does not exist."}
    concert_name = db_concert.name
    db.delete(db_concert)
    db.commit()
    return {"message": f"Concert #{concert_id} '{concert_name}' deleted."}
