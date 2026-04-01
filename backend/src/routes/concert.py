from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from crud.concert import get, get_all, create, update, delete
from database.database import get_db
from schemas.concert import ConcertCreate, ConcertResponse
from schemas.response import ApiResponse

router = APIRouter()


@router.get("/concert/", response_model=ApiResponse[List[ConcertResponse]])
async def get_all_concerts(db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get_all(db))


@router.get("/concert/{concert_id}", response_model=ApiResponse[ConcertResponse])
async def get_concert(concert_id: int, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get(db, concert_id))


@router.post("/concert/", response_model=ApiResponse[ConcertResponse])
async def create_concert(concert: ConcertCreate, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=create(db, concert))


@router.put("/concert/{concert_id}", response_model=ApiResponse[ConcertResponse])
async def update_concert(
    concert_id: int, concert: ConcertCreate, db: Session = Depends(get_db)
):
    return ApiResponse(success=True, data=update(db, concert_id, concert))


@router.delete("/concert/{concert_id}")
async def delete_concert(concert_id: int, db: Session = Depends(get_db)):
    result = delete(db, concert_id)
    return ApiResponse(success=True, data=None, message=result["message"])
