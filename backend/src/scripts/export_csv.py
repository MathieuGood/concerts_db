"""
Export the concerts database to CSV format matching data/concerts_import.csv.

Usage (run from repo root on VPS):
    docker exec concerts_db-backend-1 python src/scripts/export_csv.py > backups/concerts_$(date +%Y%m%d).csv

Automated daily backup via cron (add with: crontab -e):
    0 3 * * * docker exec concerts_db-backend-1 python src/scripts/export_csv.py > /home/ubuntu/apps/concerts_db/backups/concerts_$(date +\%Y\%m\%d).csv 2>/dev/null
"""
import sys
import csv
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.database import SessionLocal
from models.event import Event
from models.concert import Concert
from models.venue import Venue
from models.city import City
from models.attendee import Attendee
from sqlalchemy.orm import joinedload


def export_csv():
    db = SessionLocal()
    try:
        events = (
            db.query(Event)
            .options(
                joinedload(Event.venue).joinedload(Venue.city).joinedload(City.country),
                joinedload(Event.concerts).joinedload(Concert.artist),
                joinedload(Event.attendees),
                joinedload(Event.festival),
            )
            .order_by(Event.event_date)
            .all()
        )

        writer = csv.writer(sys.stdout)
        writer.writerow(["event_date", "venue", "city", "country", "artists", "attendees", "festival", "comments"])

        for event in events:
            artists = ";".join(c.artist.name for c in event.concerts)
            attendees = ";".join(
                f"{a.firstname} {a.lastname}".strip() for a in event.attendees
            )
            festival = event.festival.name if event.festival else ""
            writer.writerow([
                event.event_date,
                event.venue.name,
                event.venue.city.name,
                event.venue.city.country.name,
                artists,
                attendees,
                festival,
                event.comments or "",
            ])
    finally:
        db.close()


if __name__ == "__main__":
    export_csv()
