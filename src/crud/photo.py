from entities.Photo import Photo
from fastapi import HTTPException
from schemas.PhotoSchema import PhotoCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get(db: Session, photo_id: int):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(
            status_code=404, detail=f"Photo with ID {photo_id} not found."
        )
    return photo


def get_all(db: Session):
    return db.query(Photo).all()


def create(db: Session, photo: PhotoCreate) -> Photo:
    try:
        db_photo = Photo(name=photo.name)
        db.add(db_photo)
        db.commit()
        db.refresh(db_photo)
        return db_photo
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Photo '{db_photo.name}' already exists."
        )


def update(db: Session, photo_id: int, photo: PhotoCreate) -> Photo:
    try:
        db_photo: Photo = (
            db.query(Photo).filter(Photo.id == photo_id).first()
        )
        if db_photo is None:
            raise HTTPException(
                status_code=404, detail=f"Photo with ID {photo_id} not found."
            )
        db_photo.name = photo.name
        db.commit()
        db.refresh(db_photo)
        return db_photo
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Photo '{photo.name}' already exists."
        )


def delete(db: Session, photo_id: int):
    db_photo: Photo = (
        db.query(Photo).filter(Photo.id == photo_id).first()
    )
    if not db_photo:
        return {"message": f"Photo #{photo_id} does not exist."}
    photo_name = db_photo.name
    db.delete(db_photo)
    db.commit()
    return {"message": f"Photo #{photo_id} '{photo_name}' deleted."}
