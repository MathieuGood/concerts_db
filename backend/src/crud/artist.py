from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from models.artist import Artist
from schemas.artist import ArtistCreate


def get(db: Session, artist_id: int) -> Artist:
    artist = (
        db.query(Artist)
        .options(joinedload(Artist.country))
        .filter(Artist.id == artist_id)
        .first()
    )
    if not artist:
        raise HTTPException(
            status_code=404, detail=f"Artist with ID {artist_id} not found."
        )
    return artist


def get_all(db: Session) -> list[Artist]:
    return db.query(Artist).options(joinedload(Artist.country)).all()


def create(db: Session, artist: ArtistCreate) -> Artist:
    try:
        new_artist = Artist(name=artist.name, country_id=artist.country_id)
        db.add(new_artist)
        db.commit()
        return get(db, new_artist.id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Artist '{artist.name}' already exists."
        )


def update(db: Session, artist_id: int, artist: ArtistCreate) -> Artist:
    try:
        updated_artist = db.query(Artist).filter(Artist.id == artist_id).first()
        if updated_artist is None:
            raise HTTPException(
                status_code=404, detail=f"Artist with ID {artist_id} not found."
            )
        updated_artist.name = artist.name
        updated_artist.country_id = artist.country_id
        db.commit()
        return get(db, artist_id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Artist '{artist.name}' already exists."
        )


def delete(db: Session, artist_id: int) -> dict:
    deleted_artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not deleted_artist:
        return {"message": f"Artist #{artist_id} does not exist."}
    artist_name = deleted_artist.name
    try:
        db.delete(deleted_artist)
        db.commit()
        return {"message": f"Artist #{artist_id} '{artist_name}' deleted."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete artist '{artist_name}', they are still associated with events.",
        )
