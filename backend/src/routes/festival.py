from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from crud.festival import get, get_all, create, update, delete
from database.database import get_db
from schemas.festival import FestivalCreate, FestivalResponse
from schemas.response import ApiResponse

router = APIRouter()


@router.get("/festival/", response_model=ApiResponse[List[FestivalResponse]])
async def get_all_festivals(db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get_all(db))


@router.get("/festival/{festival_id}", response_model=ApiResponse[FestivalResponse])
async def get_festival(festival_id: int, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get(db, festival_id))


@router.post("/festival/", response_model=ApiResponse[FestivalResponse])
async def create_festival(festival: FestivalCreate, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=create(db, festival))


@router.put("/festival/{festival_id}", response_model=ApiResponse[FestivalResponse])
async def update_festival(
    festival_id: int, festival: FestivalCreate, db: Session = Depends(get_db)
):
    return ApiResponse(success=True, data=update(db, festival_id, festival))


@router.delete("/festival/{festival_id}")
async def delete_festival(festival_id: int, db: Session = Depends(get_db)):
    result = delete(db, festival_id)
    return ApiResponse(success=True, data=None, message=result["message"])
