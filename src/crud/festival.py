from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from entities.Festival import Festival
from schemas.FestivalSchema import FestivalCreate


def get(db: Session, festival_id: int):
    festival = db.query(Festival).filter(Festival.id == festival_id).first()
    if not festival:
        raise HTTPException(
            status_code=404, detail=f"Festival with ID {festival_id} not found."
        )
    return festival


def get_all(db: Session):
    return db.query(Festival).all()


def create(db: Session, festival: FestivalCreate) -> Festival:
    try:
        db_festival = Festival(name=festival.name)
        db.add(db_festival)
        db.commit()
        db.refresh(db_festival)
        return db_festival
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Festival '{db_festival.name}' already exists."
        )


def update(db: Session, festival_id: int, festival: FestivalCreate) -> Festival:
    try:
        db_festival: Festival = (
            db.query(Festival).filter(Festival.id == festival_id).first()
        )
        if db_festival is None:
            raise HTTPException(
                status_code=404, detail=f"Festival with ID {festival_id} not found."
            )
        db_festival.name = festival.name
        db.commit()
        db.refresh(db_festival)
        return db_festival
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Festival '{festival.name}' already exists."
        )


def delete(db: Session, festival_id: int):
    db_festival: Festival = (
        db.query(Festival).filter(Festival.id == festival_id).first()
    )
    if not db_festival:
        return {"message": f"Festival #{festival_id} does not exist."}
    festival_name = db_festival.name
    db.delete(db_festival)
    db.commit()
    return {"message": f"Festival #{festival_id} '{festival_name}' deleted."}
