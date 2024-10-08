from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.photo import get, get_all, create, update, delete
from database.database import get_db
from schemas.photo import PhotoCreate

router = APIRouter()


@router.get("/photo/{photo_id}")
async def get_photo(photo_id: int, db: Session = Depends(get_db)):
    return get(db, photo_id)


@router.get("/photo/")
async def get_all_photos(db: Session = Depends(get_db)):
    return get_all(db)


# Create photo
@router.post("/photo/")
async def create_photo(photo: PhotoCreate, db: Session = Depends(get_db)):
    return create(db, photo)


# Update photo
@router.put("/photo/{photo_id}")
async def update_photo(
    photo_id: int, photo: PhotoCreate, db: Session = Depends(get_db)
):
    return update(db, photo_id, photo)


# Delete photo
@router.delete("/photo/{photo_id}")
async def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    return delete(db, photo_id)
