from entities.Concert import Concert
from entities.Show import Show
from fastapi import HTTPException
from schemas.ShowSchema import ShowCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get(db: Session, show_id: int):
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(
            status_code=404, detail=f"Show with ID {show_id} not found."
        )
    show.venue.address
    show.concerts
    show.attendees
    for concert in show.concerts:
        concert.artist.address
    return show


def get_all(db: Session):
    shows = db.query(Show).all()
    for show in shows:
        show.venue.address
        show.concerts
        show.attendees
        for concert in show.concerts:
            concert.artist.address
    return shows


def create(db: Session, show: ShowCreate) -> Show:
    try:
        new_show = Show(
            name=show.name,
            event_date=show.event_date,
            comments=show.comments,
            venue_id=show.venue_id,
            festival_id=show.festival_id,
        )

        # add concerts to the show
        concerts = [concert for concert in show.concerts]
        print(f"List of all concerts for show '{show.name}':")
        print(concerts)

        for concert in show.concerts:
            new_concert = Concert()
            new_concert.artist_id = concert.artist_id
            new_concert.comments = concert.comments
            new_concert.setlist = concert.setlist
            new_concert.show = new_show

        db.add(new_show)
        db.commit()
        db.refresh(new_show)
        return new_show
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Show '{new_show.name}' already exists."
        )


def update(db: Session, show_id: int, show: ShowCreate) -> Show:
    try:
        updated_show: Show = db.query(Show).filter(Show.id == show_id).first()
        if updated_show is None:
            raise HTTPException(
                status_code=404, detail=f"Show with ID {show_id} not found."
            )
        updated_show.name = show.name
        db.commit()
        db.refresh(updated_show)
        return updated_show
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Show '{show.name}' already exists."
        )


def delete(db: Session, show_id: int):
    deleted_show: Show = db.query(Show).filter(Show.id == show_id).first()
    if not deleted_show:
        return {"message": f"Show #{show_id} does not exist."}
    show_name = deleted_show.name
    db.delete(deleted_show)
    db.commit()
    return {"message": f"Show #{show_id} '{show_name}' deleted."}
