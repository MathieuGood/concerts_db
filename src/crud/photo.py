from models.photo import Photo
from fastapi import HTTPException
from schemas.photo import PhotoCreate
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
        new_photo = Photo(path=photo.path, concert_id=photo.concert_id)
        db.add(new_photo)
        db.commit()
        db.refresh(new_photo)
        return new_photo
    except IntegrityError as e:
        print("IntegrityError")
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Photo '{new_photo.path}' already exists."
        )


def update(db: Session, photo_id: int, photo: PhotoCreate) -> Photo:
    try:
        updated_photo: Photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if updated_photo is None:
            raise HTTPException(
                status_code=404, detail=f"Photo with ID {photo_id} not found."
            )
        updated_photo.path = photo.path
        updated_photo.concert_id = photo.concert_id
        db.commit()
        db.refresh(updated_photo)
        return updated_photo
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Photo '{photo.path}' already exists."
        )


def delete(db: Session, photo_id: int):
    deleted_photo: Photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not deleted_photo:
        return {"message": f"Photo #{photo_id} does not exist."}
    db.delete(deleted_photo)
    db.commit()
    return {"message": f"Photo #{photo_id} '{deleted_photo.path}' deleted."}
