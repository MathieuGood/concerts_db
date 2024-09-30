from typing import List
from models.artist import Artist
from models.concert import Concert
from models.festival import Festival
from models.attendee import Attendee
from models.photo import Photo
from models.show import Show
from models.venue import Venue
from models.video import Video
from schemas.show import ShowCreate
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get(db: Session, show_id: int) -> Show:
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(
            status_code=404, detail=f"Show with ID {show_id} not found."
        )
    show.venue.address
    show.attendees
    show.festival
    for concert in show.concerts:
        concert.artist.address
        concert.photos
        concert.videos
    return show


def get_all(db: Session) -> List[Show]:
    shows = db.query(Show).all()
    for show in shows:
        show.venue.address
        show.attendees
        show.festival
        for concert in show.concerts:
            concert.artist.address
            concert.photos
            concert.videos
    return shows


def create(db: Session, show: ShowCreate) -> Show:
    try:
        venue = db.query(Venue).filter(Venue.id == show.venue_id).first()
        if not venue:
            raise HTTPException(
                status_code=404, detail=f"Venue with ID {show.venue_id} not found."
            )

        festival = db.query(Festival).filter(Festival.id == show.festival_id).first()
        if show.festival_id and not festival:
            raise HTTPException(
                status_code=404,
                detail=f"Festival with ID {show.festival_id} not found.",
            )

        new_show = Show(
            name=show.name,
            event_date=show.event_date,
            comments=show.comments,
            venue_id=show.venue_id,
            festival_id=show.festival_id,
        )
        db.add(new_show)
        db.commit()
        db.refresh(new_show)

        for concert in show.concerts:
            artist = db.query(Artist).filter(Artist.id == concert.artist_id).first()
            if not artist:
                raise HTTPException(
                    status_code=404,
                    detail=f"Artist with ID {concert.artist_id} not found.",
                )
            new_concert = Concert(
                comments=concert.comments,
                setlist=concert.setlist,
                show_id=new_show.id,
                artist_id=concert.artist_id,
            )

            db.add(new_concert)
            db.commit()
            db.refresh(new_concert)

            for photo_url in concert.photos:
                new_photo = Photo(path=photo_url, concert_id=new_concert.id)
                db.add(new_photo)

            for video_url in concert.videos:
                new_video = Video(path=video_url, concert_id=new_concert.id)
                db.add(new_video)

        db.commit()
        db.refresh(new_show)

        if show.attendees_ids:
            attendees = (
                db.query(Attendee).filter(Attendee.id.in_(show.attendees_ids)).all()
            )
            new_show.attendees.extend(attendees)
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
        updated_show.event_date = show.event_date
        updated_show.comments = show.comments
        updated_show.venue_id = show.venue_id
        updated_show.festival_id = show.festival_id
        updated_show.attendees_id = show.attendees_ids

        updated_show.attendees.clear()
        for attendee_id in show.attendees_ids:
            attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
            if not attendee:
                raise HTTPException(
                    status_code=404,
                    detail=f"Attendee with ID {attendee_id} not found.",
                )
            updated_show.attendees.append(attendee)

        updated_show.concerts.clear()
        new_concerts = []
        for concert in show.concerts:

            artist = db.query(Artist).filter(Artist.id == concert.artist_id).first()
            if not artist:
                raise HTTPException(
                    status_code=404,
                    detail=f"Artist with ID {concert.artist_id} not found.",
                )
            new_concert = Concert(
                comments=concert.comments,
                setlist=concert.setlist,
                show_id=updated_show.id,
                artist_id=concert.artist_id,
            )
            new_concerts.append(new_concert)

            db.add(new_concert)
            db.commit()
            db.refresh(new_concert)

            for photo_url in concert.photos:
                new_photo = Photo(path=photo_url, concert_id=new_concert.id)
                db.add(new_photo)

            for video_url in concert.videos:
                new_video = Video(path=video_url, concert_id=new_concert.id)
                db.add(new_video)

     
        db.commit()
        db.refresh(updated_show)
        return updated_show
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Show '{show.name}' already exists."
        )


def delete(db: Session, show_id: int) -> dict:
    deleted_show: Show = db.query(Show).filter(Show.id == show_id).first()
    if not deleted_show:
        return {"message": f"Show #{show_id} does not exist."}
    show_name = deleted_show.name
    db.delete(deleted_show)
    db.commit()
    return {"message": f"Show #{show_id} '{show_name}' deleted."}
