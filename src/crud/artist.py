from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from entities.Artist import Artist
from schemas.ArtistSchema import ArtistCreate


def get(db: Session, artist_id: int):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(
            status_code=404, detail=f"Artist with ID {artist_id} not found."
        )
    return artist


def get_all(db: Session):
    return db.query(Artist).all()


def create(db: Session, artist: ArtistCreate) -> Artist:
    try:
        db_artist = Artist(name=artist.name, country=artist.country)
        db.add(db_artist)
        db.commit()
        db.refresh(db_artist)
        return db_artist
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Artist '{artist.name}' already exists."
        )


def update(db: Session, artist_id: int, artist: ArtistCreate) -> Artist | HTTPException:
    try:
        db_artist: Artist | None = db.query(Artist).filter(Artist.id == artist_id).first()
        if db_artist is None:
            raise HTTPException(
                status_code=404, detail=f"Artist with ID {artist_id} not found."
            )
        db_artist.name = artist.name
        db.commit()
        db.refresh(db_artist)
        return db_artist
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Artist '{artist.name}' already exists."
        )


def delete(db: Session, artist_id: int) -> dict[str, str] | HTTPException:
    db_artist: Artist |None = db.query(Artist).filter(Artist.id == artist_id).first()
    if not db_artist:
        return {"message": f"Artist #{artist_id} does not exist."}
    artist_name = db_artist.name
    db.delete(db_artist)
    db.commit()
    return {"message": f"Artist #{artist_id} '{artist_name}' deleted."}
