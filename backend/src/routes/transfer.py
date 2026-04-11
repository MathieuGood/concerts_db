"""
Export and import routes for the concerts database.

Both routes require an admin Bearer token (same auth as /admin/*).

Export:  GET  /transfer/export
Import:  POST /transfer/import?dry_run=true|false
"""
import csv
import io
from datetime import date

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload

from auth.dependencies import require_admin
from crud import country as country_crud, city as city_crud
from database.database import get_db
from models.artist import Artist
from models.attendee import Attendee
from models.city import City
from models.concert import Concert
from models.country import Country
from models.event import Event
from models.festival import Festival
from models.user import User
from models.venue import Venue

router = APIRouter(prefix="/transfer", tags=["transfer"])

# ── CSV helpers ───────────────────────────────────────────────────────────────

HEADERS = [
    "event_date", "event_name", "venue", "city", "country",
    "festival", "artists", "concert_comments", "setlist",
    "attendees", "event_comments",
]


def _build_csv(events: list[Event]) -> str:
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(HEADERS)
    for ev in events:
        artists          = ";".join(c.artist.name for c in ev.concerts if c.artist)
        concert_comments = ";".join(c.comments or "" for c in ev.concerts)
        setlist          = ";".join(
            "|".join(line.strip() for line in (c.setlist or "").splitlines() if line.strip())
            for c in ev.concerts
        )
        attendees = ";".join(f"{a.firstname} {a.lastname}".strip() for a in ev.attendees)
        writer.writerow([
            ev.event_date,
            ev.name or "",
            ev.venue.name,
            ev.venue.city.name,
            ev.venue.city.country.name,
            ev.festival.name if ev.festival else "",
            artists,
            concert_comments,
            setlist,
            attendees,
            ev.comments or "",
        ])
    return out.getvalue()

# ── Import helpers ────────────────────────────────────────────────────────────

def _is_duplicate(db: Session, event_date: str, venue_name: str, city_name: str, country_name: str, user_id: int) -> bool:
    country = db.query(Country).filter(Country.name.ilike(country_name)).first()
    if not country:
        return False
    city = db.query(City).filter(City.name.ilike(city_name), City.country_id == country.id).first()
    if not city:
        return False
    venue = db.query(Venue).filter(Venue.name.ilike(venue_name), Venue.city_id == city.id).first()
    if not venue:
        return False
    return db.query(Event).filter(
        Event.event_date == event_date,
        Event.venue_id == venue.id,
        Event.user_id == user_id,
    ).first() is not None


def _find_or_create_venue(db: Session, name: str, city_id: int) -> Venue:
    venue = db.query(Venue).filter(Venue.name.ilike(name), Venue.city_id == city_id).first()
    if venue:
        return venue
    venue = Venue(name=name, city_id=city_id)
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue


def _find_or_create_festival(db: Session, name: str) -> Festival:
    festival = db.query(Festival).filter(Festival.name.ilike(name)).first()
    if festival:
        return festival
    festival = Festival(name=name)
    db.add(festival)
    db.commit()
    db.refresh(festival)
    return festival


def _find_or_create_artist(db: Session, name: str) -> Artist:
    artist = db.query(Artist).filter(Artist.name.ilike(name)).first()
    if artist:
        return artist
    artist = Artist(name=name)
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist


def _find_or_create_attendee(db: Session, full_name: str, user_id: int) -> Attendee:
    parts = full_name.strip().split(" ", 1)
    firstname = parts[0]
    lastname = parts[1] if len(parts) > 1 else ""
    attendee = db.query(Attendee).filter(
        Attendee.firstname.ilike(firstname),
        Attendee.lastname.ilike(lastname),
        Attendee.user_id == user_id,
    ).first()
    if attendee:
        return attendee
    attendee = Attendee(firstname=firstname, lastname=lastname, user_id=user_id)
    db.add(attendee)
    db.commit()
    db.refresh(attendee)
    return attendee

# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/export")
def export_csv(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    events = (
        db.query(Event)
        .filter(Event.user_id == current_user.id)
        .options(
            joinedload(Event.venue).joinedload(Venue.city).joinedload(City.country),
            joinedload(Event.concerts).joinedload(Concert.artist),
            joinedload(Event.attendees),
            joinedload(Event.festival),
        )
        .order_by(Event.event_date)
        .all()
    )

    csv_content = _build_csv(events)
    filename = f"concerts_{date.today().strftime('%Y%m%d')}.csv"
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/import")
async def import_csv(
    file: UploadFile = File(...),
    dry_run: bool = True,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")

    reader = csv.DictReader(io.StringIO(text))
    results: list[dict] = []

    for i, row in enumerate(reader, start=2):
        event_date    = (row.get("event_date")       or "").strip()
        venue_name    = (row.get("venue")             or "").strip()
        city_name     = (row.get("city")              or "").strip()
        country_name  = (row.get("country")           or "").strip()
        event_name    = (row.get("event_name")        or "").strip()
        festival_name = (row.get("festival")          or "").strip()
        artists_raw   = (row.get("artists")           or "").strip()
        cc_raw        = (row.get("concert_comments")  or "").strip()
        setlist_raw   = (row.get("setlist")           or "").strip()
        attendees_raw = (row.get("attendees")         or "").strip()
        event_comments = (row.get("event_comments") or row.get("comments") or "").strip()

        entry = {
            "row": i,
            "event_date": event_date,
            "venue": f"{venue_name}, {city_name}",
            "artists": artists_raw,
        }

        if not event_date or not venue_name:
            results.append({**entry, "status": "error", "reason": "Missing event_date or venue"})
            continue

        try:
            if _is_duplicate(db, event_date, venue_name, city_name, country_name, current_user.id):
                results.append({**entry, "status": "skip", "reason": "Already exists"})
                continue
        except Exception as e:
            results.append({**entry, "status": "error", "reason": str(e)})
            continue

        if dry_run:
            results.append({**entry, "status": "import"})
            continue

        try:
            country_obj = country_crud.find_or_create(db, country_name)
            city_obj    = city_crud.find_or_create(db, city_name, country_obj.id)
            venue_obj   = _find_or_create_venue(db, venue_name, city_obj.id)

            festival_id = None
            if festival_name:
                festival_id = _find_or_create_festival(db, festival_name).id

            event = Event(
                event_date=date.fromisoformat(event_date),
                name=event_name or None,
                comments=event_comments or None,
                venue_id=venue_obj.id,
                festival_id=festival_id,
                user_id=current_user.id,
            )
            db.add(event)
            db.flush()

            artists = [a.strip() for a in artists_raw.split(";") if a.strip()]
            cc_list = [c.strip() for c in cc_raw.split(";")]
            sl_list = [s.strip() for s in setlist_raw.split(";")]

            for j, artist_name in enumerate(artists):
                artist_obj = _find_or_create_artist(db, artist_name)
                c_comments = cc_list[j] if j < len(cc_list) else ""
                c_setlist  = "\n".join(sl_list[j].split("|")) if j < len(sl_list) else ""
                db.add(Concert(
                    event_id=event.id,
                    artist_id=artist_obj.id,
                    comments=c_comments or None,
                    setlist=c_setlist or None,
                ))

            if attendees_raw:
                for full_name in attendees_raw.split(";"):
                    if full_name.strip():
                        att = _find_or_create_attendee(db, full_name.strip(), current_user.id)
                        if att not in event.attendees:
                            event.attendees.append(att)

            db.commit()
            results.append({**entry, "status": "import"})

        except Exception as e:
            db.rollback()
            results.append({**entry, "status": "error", "reason": str(e)})

    return {
        "success": True,
        "data": {
            "dry_run": dry_run,
            "total": len(results),
            "imported": sum(1 for r in results if r["status"] == "import"),
            "skipped":  sum(1 for r in results if r["status"] == "skip"),
            "errors":   sum(1 for r in results if r["status"] == "error"),
            "rows": results,
        },
    }
