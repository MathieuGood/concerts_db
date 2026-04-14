"""
Export the concerts database to CSV format matching data/concerts_import.csv.

Writes to /data/backups/concerts_YYYYMMDD_HHMMSS.csv inside the container
(mounted from ~/apps/concerts_db/data/backups/ on the VPS).

Usage (on VPS):
    docker exec concerts_db-backend-1 uv run python src/scripts/export_csv.py

Automated daily backup via cron (add with: crontab -e):
    0 3 * * * docker exec concerts_db-backend-1 uv run python src/scripts/export_csv.py 2>/dev/null
"""
import sys
import csv
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.database import SessionLocal
from models.event import Event
from models.concert import Concert
from models.venue import Venue
from models.city import City
from models.attendee import Attendee
from sqlalchemy.orm import joinedload

BACKUP_DIR = Path("/data/backups")


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

        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = BACKUP_DIR / f"concerts_{timestamp}.csv"

        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["event_date", "venue", "city", "country", "artists", "i_played", "attendees", "festival", "festival_year", "comments"])

            for event in events:
                artists = ";".join(c.artist.name for c in event.concerts)
                i_played = ";".join(c.artist.name for c in event.concerts if c.i_played)
                attendees = ";".join(
                    f"{a.firstname} {a.lastname}".strip() for a in event.attendees
                )
                festival = event.festival.name if event.festival else ""
                festival_year = event.festival.year if event.festival and event.festival.year else ""
                writer.writerow([
                    event.event_date,
                    event.venue.name,
                    event.venue.city.name,
                    event.venue.city.country.name,
                    artists,
                    i_played,
                    attendees,
                    festival,
                    festival_year,
                    event.comments or "",
                ])

        print(f"Exported {len(events)} events to {output_path}")
    finally:
        db.close()


if __name__ == "__main__":
    export_csv()
