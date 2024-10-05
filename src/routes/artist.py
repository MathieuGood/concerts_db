from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.artist import get, get_all, create, update, delete
from database.database import get_db
from schemas.artist import ArtistCreate

router = APIRouter()
session = Depends(get_db)


@router.get("/artist/{artist_id}")
async def get_artist(artist_id: int, db: Session = session):
    return get(db, artist_id)


@router.get("/artist/")
async def get_all_artists(db: Session = session):
    return get_all(db)


@router.post("/artist/")
async def create_artist(artist: ArtistCreate, db: Session = session):
    return create(db, artist)


@router.put("/artist/{artist_id}")
async def update_artist(artist_id: int, artist: ArtistCreate, db: Session = session):
    return update(db, artist_id, artist)


@router.delete("/artist/{artist_id}")
async def delete_artist(artist_id: int, db: Session = session):
    return delete(db, artist_id)
