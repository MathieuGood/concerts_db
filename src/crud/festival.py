from models.festival import Festival
from fastapi import HTTPException
from schemas.festival import FestivalCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


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
        new_festival = Festival(name=festival.name)
        db.add(new_festival)
        db.commit()
        db.refresh(new_festival)
        return new_festival
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Festival '{new_festival.name}' already exists."
        )


def update(db: Session, festival_id: int, festival: FestivalCreate) -> Festival:
    try:
        updated_festival: Festival = (
            db.query(Festival).filter(Festival.id == festival_id).first()
        )
        if updated_festival is None:
            raise HTTPException(
                status_code=404, detail=f"Festival with ID {festival_id} not found."
            )
        updated_festival.name = festival.name
        db.commit()
        db.refresh(updated_festival)
        return updated_festival
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Festival '{festival.name}' already exists."
        )


def delete(db: Session, festival_id: int):
    deleted_festival: Festival = (
        db.query(Festival).filter(Festival.id == festival_id).first()
    )
    if not deleted_festival:
        return {"message": f"Festival #{festival_id} does not exist."}
    festival_name = deleted_festival.name
    db.delete(deleted_festival)
    db.commit()
    return {"message": f"Festival #{festival_id} '{festival_name}' deleted."}
