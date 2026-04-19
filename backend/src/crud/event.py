from typing import List, Optional
from models.artist import Artist
from models.city import City
from models.concert import Concert
from models.festival import Festival
from models.attendee import Attendee
from models.event import Event
from models.venue import Venue
from schemas.event import EventCreate
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload, selectinload


def _base_query(db: Session):
    """Full query for single event detail — includes artist.country."""
    return db.query(Event).options(
        joinedload(Event.venue).joinedload(Venue.city).joinedload(City.country),
        joinedload(Event.festival),
        selectinload(Event.attendees),
        selectinload(Event.concerts).joinedload(Concert.artist).joinedload(Artist.country),
    )


def _list_query(db: Session):
    """Lighter query for list — omits artist.country."""
    return db.query(Event).options(
        joinedload(Event.venue).joinedload(Venue.city).joinedload(City.country),
        joinedload(Event.festival),
        selectinload(Event.attendees),
        selectinload(Event.concerts).joinedload(Concert.artist),
    )


def get(db: Session, event_id: int, user_id: Optional[int] = None) -> Event:
    q = _base_query(db).filter(Event.id == event_id)
    if user_id is not None:
        q = q.filter(Event.user_id == user_id)
    event = q.first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with ID {event_id} not found.")
    event.concerts = sorted(event.concerts, key=lambda c: c.id)
    return event


def get_all(db: Session, user_id: Optional[int] = None) -> List[Event]:
    q = _list_query(db)
    if user_id is not None:
        q = q.filter(Event.user_id == user_id)
    return q.order_by(Event.event_date.desc()).all()


def create(db: Session, event: EventCreate, user_id: int) -> Event:
    try:
        venue = db.query(Venue).filter(Venue.id == event.venue_id).first()
        if not venue:
            raise HTTPException(status_code=404, detail=f"Venue with ID {event.venue_id} not found.")

        if event.festival_id:
            festival = db.query(Festival).filter(Festival.id == event.festival_id).first()
            if not festival:
                raise HTTPException(status_code=404, detail=f"Festival with ID {event.festival_id} not found.")

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
                raise HTTPException(status_code=404, detail=f"Artist with ID {concert.artist_id} not found.")
            db.add(Concert(
                comments=concert.comments,
                setlist=concert.setlist,
                i_played=concert.i_played,
                event_id=new_event.id,
                artist_id=concert.artist_id,
            ))

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
        raise HTTPException(status_code=409, detail=f"You already have an event at this venue on {event.event_date}.")


def update(db: Session, event_id: int, event: EventCreate, user_id: int) -> Event:
    try:
        updated_event: Event = (
            db.query(Event).filter(Event.id == event_id, Event.user_id == user_id).first()
        )
        if updated_event is None:
            raise HTTPException(status_code=404, detail=f"Event with ID {event_id} not found.")

        updated_event.name = event.name
        updated_event.event_date = event.event_date
        updated_event.comments = event.comments
        updated_event.venue_id = event.venue_id
        updated_event.festival_id = event.festival_id

        updated_event.attendees.clear()
        if event.attendees_ids:
            attendees = (
                db.query(Attendee)
                .filter(Attendee.id.in_(event.attendees_ids), Attendee.user_id == user_id)
                .all()
            )
            if len(attendees) != len(event.attendees_ids):
                raise HTTPException(status_code=403, detail="One or more attendees not found or do not belong to you.")
            updated_event.attendees.extend(attendees)

        updated_event.concerts.clear()
        updated_concerts = []

        for concert in event.concerts:
            existing = (
                db.query(Concert)
                .filter(Concert.id == concert.id, Concert.event_id == event_id)
                .first()
            )
            if existing:
                existing.event_id = updated_event.id
                existing.comments = concert.comments
                existing.setlist = concert.setlist
                existing.i_played = concert.i_played
                existing.artist_id = concert.artist_id
                existing.artist = db.query(Artist).filter(Artist.id == concert.artist_id).first()
                updated_concerts.append(existing)
            else:
                artist = db.query(Artist).filter(Artist.id == concert.artist_id).first()
                if not artist:
                    raise HTTPException(status_code=404, detail=f"Artist with ID {concert.artist_id} not found.")
                updated_concerts.append(Concert(
                    comments=concert.comments,
                    setlist=concert.setlist,
                    i_played=concert.i_played,
                    event_id=updated_event.id,
                    artist_id=concert.artist_id,
                    artist=artist,
                ))

        updated_event.concerts.extend(updated_concerts)
        db.commit()
        db.refresh(updated_event)
        return updated_event

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"You already have an event at this venue on {event.event_date}.")


def delete(db: Session, event_id: int, user_id: int) -> dict:
    event = db.query(Event).filter(Event.id == event_id, Event.user_id == user_id).first()
    if not event:
        return {"message": f"Event #{event_id} does not exist."}
    desc = f"{event.name} at {event.venue.name} on {event.event_date}"
    db.delete(event)
    db.commit()
    return {"message": f"Event #{event_id} '{desc}' deleted."}
