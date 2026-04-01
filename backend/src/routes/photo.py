from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from crud.photo import get, get_all, create, update, delete
from database.database import get_db
from schemas.photo import PhotoCreate, PhotoResponse
from schemas.response import ApiResponse

router = APIRouter()


@router.get("/photo/", response_model=ApiResponse[List[PhotoResponse]])
async def get_all_photos(db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get_all(db))


@router.get("/photo/{photo_id}", response_model=ApiResponse[PhotoResponse])
async def get_photo(photo_id: int, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get(db, photo_id))


@router.post("/photo/", response_model=ApiResponse[PhotoResponse])
async def create_photo(photo: PhotoCreate, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=create(db, photo))


@router.put("/photo/{photo_id}", response_model=ApiResponse[PhotoResponse])
async def update_photo(
    photo_id: int, photo: PhotoCreate, db: Session = Depends(get_db)
):
    return ApiResponse(success=True, data=update(db, photo_id, photo))


@router.delete("/photo/{photo_id}")
async def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    result = delete(db, photo_id)
    return ApiResponse(success=True, data=None, message=result["message"])
