from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from crud.country import get, get_all, create, update, delete
from database.database import get_db
from schemas.country import CountryCreate, CountryResponse
from schemas.response import ApiResponse
from auth.dependencies import get_current_user
from models.user import User

router = APIRouter()


@router.get("/country/", response_model=ApiResponse[List[CountryResponse]])
async def get_all_countries(db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get_all(db))


@router.get("/country/{country_id}", response_model=ApiResponse[CountryResponse])
async def get_country(country_id: int, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get(db, country_id))


@router.post("/country/", response_model=ApiResponse[CountryResponse])
async def create_country(country: CountryCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return ApiResponse(success=True, data=create(db, country))


@router.put("/country/{country_id}", response_model=ApiResponse[CountryResponse])
async def update_country(
    country_id: int, country: CountryCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    return ApiResponse(success=True, data=update(db, country_id, country))


@router.delete("/country/{country_id}")
async def delete_country(country_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    result = delete(db, country_id)
    return ApiResponse(success=True, data=None, message=result["message"])
