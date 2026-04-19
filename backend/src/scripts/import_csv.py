"""
Import concerts from a CSV file into the database.

Usage (on VPS):
    docker exec concerts_db-backend-1 uv run python src/scripts/import_csv.py
    docker exec concerts_db-backend-1 uv run python src/scripts/import_csv.py --file /data/hellfest_2006.csv

The default CSV is volume-mounted at /data/concerts_import.csv inside the container.
Already-existing events (same date + venue) are skipped safely.
"""
import argparse
import csv
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.database import SessionLocal
from models.event import Event
from models.concert import Concert
from models.venue import Venue
from models.artist import Artist
from models.attendee import Attendee
from models.festival import Festival
from models.user import User  # noqa: F401 — needed for SQLAlchemy FK resolution
from sqlalchemy.orm import Session
from crud import country as country_crud
from crud import city as city_crud

DEFAULT_CSV_PATH = Path("/data/concerts_import.csv")


def find_or_create_venue(db: Session, name: str, city_id: int) -> Venue:
    venue = db.query(Venue).filter(Venue.name.ilike(name.strip()), Venue.city_id == city_id).first()
    if venue:
        return venue
    venue = Venue(name=name.strip(), city_id=city_id)
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue


def find_or_create_festival(db: Session, name: str, year: int | None = None) -> Festival:
    query = db.query(Festival).filter(Festival.name.ilike(name.strip()))
    if year is not None:
        query = query.filter(Festival.year == year)
    else:
        query = query.filter(Festival.year.is_(None))
    festival = query.first()
    if festival:
        return festival
    festival = Festival(name=name.strip(), year=year)
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


def import_csv(csv_path: Path = DEFAULT_CSV_PATH):
    if not csv_path.exists():
        print(f"ERROR: CSV not found at {csv_path}")
        sys.exit(1)

    db = SessionLocal()
    imported = 0
    skipped = 0
    errors = 0

    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                event_date  = row["event_date"].strip()
                venue_name  = row["venue"].strip()
                city_name   = row["city"].strip()
                country_name = row["country"].strip()
                artists_raw  = row["artists"].strip()
                attendees_raw = row["attendees"].strip()
                festival_name = row["festival"].strip()
                festival_year_raw = row.get("festival_year", "").strip()
                festival_year = int(festival_year_raw) if festival_year_raw else None
                comments    = row["comments"].strip()
                i_played_raw = row.get("i_played", "").strip().lower()
                i_played_artists = set(i_played_raw.split(";")) if i_played_raw else set()

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
                        festival_id = find_or_create_festival(db, festival_name, festival_year).id

                    event = Event(
                        event_date=date.fromisoformat(event_date),
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
                            played = artist_name.strip().lower() in i_played_artists
                            db.add(Concert(event_id=event.id, artist_id=artist.id, i_played=played))

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, default=DEFAULT_CSV_PATH, help="Path to CSV file inside the container")
    args = parser.parse_args()
    import_csv(args.file)
