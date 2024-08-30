from entities.Show import Show
from fastapi import HTTPException
from schemas.ShowSchema import ShowCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get(db: Session, show_id: int):
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(
            status_code=404, detail=f"Show with ID {show_id} not found."
        )
    return show


def get_all(db: Session):
    return db.query(Show).all()


def create(db: Session, show: ShowCreate) -> Show:
    try:
        db_show = Show(name=show.name)
        db.add(db_show)
        db.commit()
        db.refresh(db_show)
        return db_show
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Show '{db_show.name}' already exists."
        )


def update(db: Session, show_id: int, show: ShowCreate) -> Show:
    try:
        db_show: Show = (
            db.query(Show).filter(Show.id == show_id).first()
        )
        if db_show is None:
            raise HTTPException(
                status_code=404, detail=f"Show with ID {show_id} not found."
            )
        db_show.name = show.name
        db.commit()
        db.refresh(db_show)
        return db_show
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Show '{show.name}' already exists."
        )


def delete(db: Session, show_id: int):
    db_show: Show = (
        db.query(Show).filter(Show.id == show_id).first()
    )
    if not db_show:
        return {"message": f"Show #{show_id} does not exist."}
    show_name = db_show.name
    db.delete(db_show)
    db.commit()
    return {"message": f"Show #{show_id} '{show_name}' deleted."}
