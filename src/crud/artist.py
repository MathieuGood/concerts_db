from entities.address import Address
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from entities.artist import Artist
from schemas.artist import ArtistCreate


def get(db: Session, artist_id: int) -> Artist:
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(
            status_code=404, detail=f"Artist with ID {artist_id} not found."
        )
    return artist


def get_all(db: Session) -> list[Artist]:
    return db.query(Artist).all()


def create(db: Session, artist: ArtistCreate) -> Artist:
    try:
        address: Address | None = (
            db.query(Address).filter(Address.id == artist.address_id).first()
        )
        if not address:
            raise HTTPException(
                status_code=404,
                detail=f"Address with ID {artist.address_id} not found.",
            )

        new_artist = Artist(name=artist.name, address=address)
        db.add(new_artist)
        db.commit()
        db.refresh(new_artist)
        return new_artist
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Artist '{artist.name}' already exists."
        )


def update(db: Session, artist_id: int, artist: ArtistCreate) -> Artist | HTTPException:
    try:
        updated_artist: Artist | None = (
            db.query(Artist).filter(Artist.id == artist_id).first()
        )
        if updated_artist is None:
            raise HTTPException(
                status_code=404, detail=f"Artist with ID {artist_id} not found."
            )
        updated_artist.name = artist.name
        db.commit()
        db.refresh(updated_artist)
        return updated_artist
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Artist '{artist.name}' already exists."
        )


def delete(db: Session, artist_id: int) -> dict[str, str] | HTTPException:
    deleted_artist: Artist | None = (
        db.query(Artist).filter(Artist.id == artist_id).first()
    )
    if not deleted_artist:
        return {"message": f"Artist #{artist_id} does not exist."}
    artist_name = deleted_artist.name
    db.delete(deleted_artist)
    db.commit()
    return {"message": f"Artist #{artist_id} '{artist_name}' deleted."}
