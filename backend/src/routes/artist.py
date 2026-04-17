from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from crud.artist import get, get_all, create, update, delete
from database.database import get_db
from schemas.artist import ArtistCreate, ArtistResponse
from schemas.response import ApiResponse
from auth.dependencies import get_current_user
from models.user import User

router = APIRouter()


@router.get("/artist/", response_model=ApiResponse[List[ArtistResponse]])
async def get_all_artists(db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get_all(db))


@router.get("/artist/{artist_id}", response_model=ApiResponse[ArtistResponse])
async def get_artist(artist_id: int, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get(db, artist_id))


@router.post("/artist/", response_model=ApiResponse[ArtistResponse])
async def create_artist(artist: ArtistCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return ApiResponse(success=True, data=create(db, artist))


@router.put("/artist/{artist_id}", response_model=ApiResponse[ArtistResponse])
async def update_artist(
    artist_id: int, artist: ArtistCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    return ApiResponse(success=True, data=update(db, artist_id, artist))


@router.delete("/artist/{artist_id}")
async def delete_artist(artist_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    result = delete(db, artist_id)
    return ApiResponse(success=True, data=None, message=result["message"])
