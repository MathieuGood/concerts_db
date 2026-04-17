from typing import List, Optional
from models.artist import Artist
from models.city import City
from models.concert import Concert
from models.festival import Festival
from models.attendee import Attendee
from models.photo import Photo
from models.event import Event
from models.venue import Venue
from models.video import Video
from schemas.event import EventCreate
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload


def _base_query(db: Session):
    return db.query(Event).options(
        joinedload(Event.venue).joinedload(Venue.city).joinedload(City.country),
        joinedload(Event.attendees),
        joinedload(Event.festival),
        joinedload(Event.concerts).joinedload(Concert.artist).joinedload(Artist.country),
        joinedload(Event.concerts).joinedload(Concert.photos),
        joinedload(Event.concerts).joinedload(Concert.videos),
    )


def get(db: Session, event_id: int, user_id: Optional[int] = None) -> Event:
    q = _base_query(db).filter(Event.id == event_id)
    if user_id is not None:
        q = q.filter(Event.user_id == user_id)
    event = q.first()
    if not event:
        raise HTTPException(
            status_code=404, detail=f"Event with ID {event_id} not found."
        )
    event.concerts = sorted(event.concerts, key=lambda concert: concert.id)
    return event


def get_all(db: Session, user_id: Optional[int] = None) -> List[Event]:
    q = _base_query(db)
    if user_id is not None:
        q = q.filter(Event.user_id == user_id)
    return q.order_by(Event.event_date.desc()).all()


def create(db: Session, event: EventCreate, user_id: int) -> Event:
    try:
        venue = db.query(Venue).filter(Venue.id == event.venue_id).first()
        if not venue:
            raise HTTPException(
                status_code=404, detail=f"Venue with ID {event.venue_id} not found."
            )

        if event.festival_id:
            festival = db.query(Festival).filter(Festival.id == event.festival_id).first()
            if not festival:
                raise HTTPException(
                    status_code=404,
                    detail=f"Festival with ID {event.festival_id} not found.",
                )

        new_event = Event(
            name=event.name,
            event_date=event.event_date,
            comments=event.comments,
            venue_id=event.venue_id,
            festival_id=event.festival_id,
            user_id=user_id,
        )
        db.add(new_event)
        db.commit()
        db.refresh(new_event)

        for concert in event.concerts:
            artist = db.query(Artist).filter(Artist.id == concert.artist_id).first()
            if not artist:
                raise HTTPException(
                    status_code=404,
                    detail=f"Artist with ID {concert.artist_id} not found.",
                )
            new_concert = Concert(
                comments=concert.comments,
                setlist=concert.setlist,
                i_played=concert.i_played,
                event_id=new_event.id,
                artist_id=concert.artist_id,
            )

            db.add(new_concert)
            db.commit()
            db.refresh(new_concert)

            update_concert_photos(db, concert, new_concert)
            update_concert_videos(db, concert, new_concert)

        db.commit()
        db.refresh(new_event)

        if event.attendees_ids:
            attendees = (
                db.query(Attendee)
                .filter(Attendee.id.in_(event.attendees_ids), Attendee.user_id == user_id)
                .all()
            )
            if len(attendees) != len(event.attendees_ids):
                raise HTTPException(status_code=403, detail="One or more attendees do not belong to you.")
            new_event.attendees.extend(attendees)
            db.commit()
            db.refresh(new_event)

        return new_event

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"You already have an event at this venue on {event.event_date}.",
        )


def update(db: Session, event_id: int, event: EventCreate, user_id: int) -> Event:
    try:
        updated_event: Event = db.query(Event).filter(Event.id == event_id, Event.user_id == user_id).first()
        if updated_event is None:
            raise HTTPException(
                status_code=404, detail=f"Event with ID {event_id} not found."
            )

        updated_event.name = event.name
        updated_event.event_date = event.event_date
        updated_event.comments = event.comments
        updated_event.venue_id = event.venue_id
        updated_event.festival_id = event.festival_id

        updated_event.attendees.clear()
        for attendee_id in event.attendees_ids:
            attendee = db.query(Attendee).filter(Attendee.id == attendee_id, Attendee.user_id == user_id).first()
            if not attendee:
                raise HTTPException(
                    status_code=403,
                    detail=f"Attendee with ID {attendee_id} not found or does not belong to you.",
                )
            updated_event.attendees.append(attendee)

        updated_event.concerts.clear()
        updated_concerts = []

        for concert in event.concerts:
            existing_concert = (
                db.query(Concert).filter(Concert.id == concert.id, Concert.event_id == event_id).first()
            )

            if existing_concert:
                existing_concert.event_id = updated_event.id
                existing_concert.comments = concert.comments
                existing_concert.setlist = concert.setlist
                existing_concert.i_played = concert.i_played
                existing_concert.artist_id = concert.artist_id
                existing_concert.artist = (
                    db.query(Artist).filter(Artist.id == concert.artist_id).first()
                )
                update_concert_photos(db, concert, existing_concert)
                update_concert_videos(db, concert, existing_concert)
                updated_concerts.append(existing_concert)
            else:
                artist = db.query(Artist).filter(Artist.id == concert.artist_id).first()
                if not artist:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Artist with ID {concert.artist_id} not found.",
                    )
                new_concert = Concert(
                    comments=concert.comments,
                    setlist=concert.setlist,
                    i_played=concert.i_played,
                    event_id=updated_event.id,
                    artist_id=concert.artist_id,
                    artist=artist,
                )
                update_concert_photos(db, concert, new_concert)
                update_concert_videos(db, concert, new_concert)
                updated_concerts.append(new_concert)

        updated_event.concerts.extend(updated_concerts)
        db.commit()
        db.refresh(updated_event)
        return updated_event

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"You already have an event at this venue on {event.event_date}.",
        )


def update_concert_photos(
    db: Session, concert_data: Concert, concert_to_update: Concert
):
    concert_to_update.photos.clear()
    if concert_data.photos_ids:
        for photo_id in concert_data.photos_ids:
            photo = db.query(Photo).filter(Photo.id == photo_id).first()
            if not photo:
                raise HTTPException(
                    status_code=404,
                    detail=f"Photo with ID {photo_id} not found.",
                )
            concert_to_update.photos.append(photo)


def update_concert_videos(
    db: Session, concert_data: Concert, concert_to_update: Concert
):
    concert_to_update.videos.clear()
    if concert_data.videos_ids:
        for video_id in concert_data.videos_ids:
            video = db.query(Video).filter(Video.id == video_id).first()
            if not video:
                raise HTTPException(
                    status_code=404,
                    detail=f"Video with ID {video_id} not found.",
                )
            concert_to_update.videos.append(video)


def delete(db: Session, event_id: int, user_id: int) -> dict:
    deleted_event: Event = db.query(Event).filter(Event.id == event_id, Event.user_id == user_id).first()
    if not deleted_event:
        return {"message": f"Event #{event_id} does not exist."}
    event_desc = (
        f"{deleted_event.name} at {deleted_event.venue.name} on {deleted_event.event_date}"
    )
    db.delete(deleted_event)
    db.commit()
    return {"message": f"Event #{event_id} '{event_desc}' deleted."}
