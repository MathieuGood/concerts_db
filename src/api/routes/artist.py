from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.artist import get, get_all, create, update, delete
from database.database import get_db
from entities.Artist import Artist
from schemas.ArtistSchema import ArtistCreate

router = APIRouter()
session = Depends(get_db)

router = APIRouter()


@router.get("/artist/{artist_id}")
def get_artist(artist_id: int, db: Session = session):
    return get(db, artist_id)


@router.get("/artist/")
def get_all_artists(db: Session = session):
    return get_all(db)


# Create artist
@router.post("/artist/")
def create_artist(artist: ArtistCreate, db: Session = session):
    return create(db, artist)


# Update artist
@router.put("/artist/{artist_id}")
def update_artist(artist_id: int, artist: ArtistCreate, db: Session = session):
    return update(db, artist_id, artist)


# Delete artist
@router.delete("/artist/{artist_id}")
def delete_artist(artist_id: int, db: Session = session):
    return delete(db, artist_id)
