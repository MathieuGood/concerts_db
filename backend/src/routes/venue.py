from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from crud.venue import get, get_all, create, update, delete
from database.database import get_db
from schemas.venue import VenueCreate, VenueResponse
from schemas.response import ApiResponse
from auth.dependencies import get_current_user
from models.user import User

router = APIRouter()


@router.get("/venue/", response_model=ApiResponse[List[VenueResponse]])
async def get_all_venues(db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get_all(db))


@router.get("/venue/{venue_id}", response_model=ApiResponse[VenueResponse])
async def get_venue(venue_id: int, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get(db, venue_id))


@router.post("/venue/", response_model=ApiResponse[VenueResponse])
async def create_venue(venue: VenueCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return ApiResponse(success=True, data=create(db, venue))


@router.put("/venue/{venue_id}", response_model=ApiResponse[VenueResponse])
async def update_venue(
    venue_id: int, venue: VenueCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    return ApiResponse(success=True, data=update(db, venue_id, venue))


@router.delete("/venue/{venue_id}")
async def delete_venue(venue_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    result = delete(db, venue_id)
    return ApiResponse(success=True, data=None, message=result["message"])
