"""
Import concerts from data/concerts_import.csv into the database.

Usage (on VPS):
    docker exec concerts_db-backend-1 python src/scripts/import_csv.py

The CSV is volume-mounted at /data/concerts_import.csv inside the container.
Already-existing events (same date + venue) are skipped safely.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.database import SessionLocal
from models.event import Event
from models.concert import Concert
from models.venue import Venue
from models.artist import Artist
from models.attendee import Attendee
from models.festival import Festival
from sqlalchemy.orm import Session
from crud import country as country_crud
from crud import city as city_crud

CSV_PATH = Path("/data/concerts_import.csv")


def find_or_create_venue(db: Session, name: str, city_id: int) -> Venue:
    venue = db.query(Venue).filter(Venue.name.ilike(name.strip()), Venue.city_id == city_id).first()
    if venue:
        return venue
    venue = Venue(name=name.strip(), city_id=city_id)
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue


def find_or_create_festival(db: Session, name: str) -> Festival:
    festival = db.query(Festival).filter(Festival.name.ilike(name.strip())).first()
    if festival:
        return festival
    festival = Festival(name=name.strip())
    db.add(festival)
    db.commit()
    db.refresh(festival)
    return festival


def find_or_create_artist(db: Session, name: str) -> Artist:
    artist = db.query(Artist).filter(Artist.name.ilike(name.strip())).first()
    if artist:
        return artist
    artist = Artist(name=name.strip())
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist


def find_or_create_attendee(db: Session, full_name: str) -> Attendee:
    parts = full_name.strip().split(" ", 1)
    firstname = parts[0]
    lastname = parts[1] if len(parts) > 1 else ""
    attendee = db.query(Attendee).filter(
        Attendee.firstname.ilike(firstname),
        Attendee.lastname.ilike(lastname),
    ).first()
    if attendee:
        return attendee
    attendee = Attendee(firstname=firstname, lastname=lastname)
    db.add(attendee)
    db.commit()
    db.refresh(attendee)
    return attendee


def import_csv():
    if not CSV_PATH.exists():
        print(f"ERROR: CSV not found at {CSV_PATH}")
        sys.exit(1)

    db = SessionLocal()
    imported = 0
    skipped = 0
    errors = 0

    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                event_date  = row["event_date"].strip()
                venue_name  = row["venue"].strip()
                city_name   = row["city"].strip()
                country_name = row["country"].strip()
                artists_raw  = row["artists"].strip()
                attendees_raw = row["attendees"].strip()
                festival_name = row["festival"].strip()
                comments    = row["comments"].strip()

                if not event_date or not venue_name:
                    continue

                try:
                    country = country_crud.find_or_create(db, country_name)
                    city    = city_crud.find_or_create(db, city_name, country.id)
                    venue   = find_or_create_venue(db, venue_name, city.id)

                    existing = db.query(Event).filter(
                        Event.event_date == event_date,
                        Event.venue_id == venue.id,
                    ).first()
                    if existing:
                        print(f"SKIP  {event_date} @ {venue_name} ({city_name})")
                        skipped += 1
                        continue

                    festival_id = None
                    if festival_name:
                        festival_id = find_or_create_festival(db, festival_name).id

                    event = Event(
                        event_date=event_date,
                        comments=comments,
                        venue_id=venue.id,
                        festival_id=festival_id,
                    )
                    db.add(event)
                    db.commit()
                    db.refresh(event)

                    for artist_name in artists_raw.split(";"):
                        if artist_name.strip():
                            artist = find_or_create_artist(db, artist_name.strip())
                            db.add(Concert(event_id=event.id, artist_id=artist.id))

                    if attendees_raw:
                        for full_name in attendees_raw.split(";"):
                            if full_name.strip():
                                attendee = find_or_create_attendee(db, full_name.strip())
                                if attendee not in event.attendees:
                                    event.attendees.append(attendee)

                    db.commit()
                    print(f"OK    {event_date} @ {venue_name} ({city_name}) — {artists_raw}")
                    imported += 1

                except Exception as e:
                    db.rollback()
                    print(f"ERROR {event_date} @ {venue_name}: {e}")
                    errors += 1

    finally:
        db.close()

    print(f"\n{'='*50}")
    print(f"Imported: {imported} | Skipped: {skipped} | Errors: {errors}")


if __name__ == "__main__":
    import_csv()
