from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.photo import get, get_all, create, update, delete
from database.database import get_db
from schemas.photo import PhotoCreate

router = APIRouter()
session = Depends(get_db)

router = APIRouter()


@router.get("/photo/{photo_id}")
def get_photo(photo_id: int, db: Session = session):
    return get(db, photo_id)


@router.get("/photo/")
def get_all_photos(db: Session = session):
    return get_all(db)


# Create photo
@router.post("/photo/")
def create_photo(photo: PhotoCreate, db: Session = session):
    return create(db, photo)


# Update photo
@router.put("/photo/{photo_id}")
def update_photo(photo_id: int, photo: PhotoCreate, db: Session = session):
    return update(db, photo_id, photo)


# Delete photo
@router.delete("/photo/{photo_id}")
def delete_photo(photo_id: int, db: Session = session):
    return delete(db, photo_id)
