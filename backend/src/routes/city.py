from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from crud.city import get, get_all, create, update, delete
from database.database import get_db
from schemas.city import CityCreate, CityResponse
from schemas.response import ApiResponse

router = APIRouter()


@router.get("/city/", response_model=ApiResponse[List[CityResponse]])
async def get_all_cities(country_id: Optional[int] = None, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get_all(db, country_id))


@router.get("/city/{city_id}", response_model=ApiResponse[CityResponse])
async def get_city(city_id: int, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get(db, city_id))


@router.post("/city/", response_model=ApiResponse[CityResponse])
async def create_city(city: CityCreate, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=create(db, city))


@router.put("/city/{city_id}", response_model=ApiResponse[CityResponse])
async def update_city(
    city_id: int, city: CityCreate, db: Session = Depends(get_db)
):
    return ApiResponse(success=True, data=update(db, city_id, city))


@router.delete("/city/{city_id}")
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    result = delete(db, city_id)
    return ApiResponse(success=True, data=None, message=result["message"])
