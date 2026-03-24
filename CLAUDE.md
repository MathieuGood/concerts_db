# concerts_db — Project Reference & Refactoring Progress

## How to run

```bash
# Backend
cd backend
uv run uvicorn main:app --reload --app-dir src
# → http://127.0.0.1:8000

# Frontend
cd frontend
npm run dev
```

The SQLite DB (`backend/flask_concerts_db.sqlite`) auto-creates on first startup via `Base.metadata.create_all()` in the lifespan.
To reset with seed data: set `DEMO_MODE=TRUE` in `backend/.env`, restart once, then set back to `FALSE`.

---

## Tech stack

**Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 (ORM), Pydantic v2, SQLite (dev) / PostgreSQL (prod), uvicorn, uv (package manager)

**Frontend:** React 18, TypeScript, Vite, React Router v6, MUI v6, Axios, Tailwind CSS, dayjs

---

## Project structure

```
concerts_db/
├── backend/
│   ├── .env                          # DB URI + DEMO_MODE flag (not committed)
│   ├── pyproject.toml                # uv project config
│   ├── uv.lock
│   ├── flask_concerts_db.sqlite      # local SQLite DB (auto-created)
│   └── src/
│       ├── main.py                   # FastAPI app + lifespan + router registration
│       ├── config.py                 # Config class reading .env
│       ├── database/
│       │   └── database.py           # engine, SessionLocal, get_db(), seed_data()
│       ├── models/                   # SQLAlchemy ORM models
│       │   ├── base.py
│       │   ├── address.py
│       │   ├── artist.py
│       │   ├── attendee.py
│       │   ├── concert.py
│       │   ├── event.py
│       │   ├── event_attendee_association.py
│       │   ├── festival.py
│       │   ├── photo.py
│       │   ├── venue.py
│       │   └── video.py
│       ├── schemas/                  # Pydantic request/response schemas
│       │   ├── address.py
│       │   ├── artist.py
│       │   ├── attendee.py
│       │   ├── concert.py
│       │   ├── event.py
│       │   ├── festival.py
│       │   ├── photo.py
│       │   ├── venue.py
│       │   └── video.py
│       ├── crud/                     # Business logic / DB operations
│       │   ├── address.py
│       │   ├── artist.py
│       │   ├── attendee.py
│       │   ├── concert.py
│       │   ├── event.py
│       │   ├── festival.py
│       │   ├── photo.py
│       │   ├── venue.py
│       │   └── video.py
│       ├── routes/                   # FastAPI routers
│       │   ├── root.py
│       │   ├── address.py
│       │   ├── artist.py
│       │   ├── attendee.py
│       │   ├── concert.py
│       │   ├── event.py
│       │   ├── festival.py
│       │   ├── photo.py
│       │   ├── venue.py
│       │   └── video.py
│       ├── repositories/             # Thin repository wrappers over BaseRepository
│       │   ├── base.py
│       │   ├── address.py / artist.py / attendee.py / concert.py
│       │   ├── event.py / festival.py / photo.py / venue.py / video.py
│       └── mockup_data/
│           └── concerts_mock_data.py # Seed data (used in DEMO_MODE)
└── frontend/
    └── src/
        ├── components/
        ├── models/
        ├── pages/
        └── services/
```

---

## Data model

### Conceptual summary

An **Event** is a live music night at a **Venue** on a specific date. It optionally belongs to a **Festival**. It has one or more **Concerts** (each Concert = one artist performing that night). **Attendees** are people who attended the event (many-to-many). Each **Concert** can have **Photos** and **Videos**.

```
Address ──────────────────── Venue
   └── Artist                  └── Event ──── Festival (optional)
          └── Concert ◄──────────── Event
                  ├── Photo         └── Attendees (M2M)
                  └── Video
```

### DB tables & key fields

| Table | Key columns | Notes |
|-------|-------------|-------|
| `addresses` | `id`, `city`, `country` | Unique: (city, country) |
| `artists` | `id`, `name`, `address_id` | `name` unique |
| `venues` | `id`, `name`, `address_id` | Unique: (name, address_id) |
| `festivals` | `id`, `name` | `name` unique |
| `events` | `id`, `name`, `event_date`, `comments`, `venue_id`, `festival_id` | Unique: (event_date, venue_id); festival optional |
| `event_attendees` | `event_id`, `attendee_id` | M2M join table; CASCADE on event delete, RESTRICT on attendee delete |
| `attendees` | `id`, `firstname`, `lastname` | Unique: (firstname, lastname) |
| `concerts` | `id`, `comments`, `setlist`, `event_id`, `artist_id` | Cascade deleted with event |
| `photos` | `id`, `path`, `concert_id` | Unique: (path, concert_id); cascade deleted with concert |
| `videos` | `id`, `path`, `concert_id` | Unique: (path, concert_id); cascade deleted with concert |

### Relationships

| From | To | Type |
|------|----|------|
| Address | Venue | 1:Many |
| Address | Artist | 1:Many |
| Venue | Event | 1:Many |
| Festival | Event | 1:Many (optional FK) |
| Event | Concert | 1:Many (cascade delete) |
| Event | Attendee | Many:Many via `event_attendees` |
| Artist | Concert | 1:Many |
| Concert | Photo | 1:Many (cascade delete) |
| Concert | Video | 1:Many (cascade delete) |

---

## API endpoints

All resources follow the same CRUD pattern. **Note: list endpoints (`GET /resource/`) currently have a route ordering bug — see issues below.**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET/POST | `/address/`, `/address/{id}`, PUT, DELETE | Address CRUD |
| GET/POST | `/artist/`, `/artist/{id}`, PUT, DELETE | Artist CRUD |
| GET/POST | `/attendee/`, `/attendee/{id}`, PUT, DELETE | Attendee CRUD |
| GET/POST | `/concert/`, `/concert/{id}`, PUT, DELETE | Concert CRUD |
| GET/POST | `/event/`, `/event/{id}`, PUT, DELETE | Event CRUD |
| GET/POST | `/festival/`, `/festival/{id}`, PUT, DELETE | Festival CRUD |
| GET/POST | `/venue/`, `/venue/{id}`, PUT, DELETE | Venue CRUD |
| GET/POST | `/photo/`, `/photo/{id}`, PUT, DELETE | Photo CRUD |
| GET/POST | `/video/`, `/video/{id}`, PUT, DELETE | Video CRUD |

---

## Schema shapes (key ones)

**EventCreate** — body for POST/PUT `/event/`
```json
{
  "name": "NOFX Final Tour",
  "event_date": "2024-06-01",
  "comments": "...",
  "venue_id": 1,
  "festival_id": 5,
  "attendees_ids": [1, 2],
  "concerts": [
    { "id": null, "artist_id": 3, "comments": "...", "setlist": "...", "photos_ids": [], "videos_ids": [] }
  ]
}
```

**ConcertCreate** — embedded in EventCreate or standalone POST `/concert/`
```json
{ "id": null, "event_id": 1, "artist_id": 3, "comments": "...", "setlist": "...", "photos_ids": [1, 2], "videos_ids": [1] }
```

---

## What has been done (refactoring log)

### Session 1 (2026-03-24)

**Removed all tests**
- Deleted `backend/src/tests/` and root `OLD_pyproject.toml`

**Fixed startup & dependencies**
- `pyproject.toml`: `dotenv` → `python-dotenv`, `psycopg2` → `psycopg2-binary`, added `uvicorn`
- `database.py`: removed `Base.metadata.create_all()` and debug print from `get_db()` — now called once in lifespan
- `main.py`: removed redundant `app.router.lifespan_context`, unused imports
- `.env`: switched to local SQLite, `DEMO_MODE=FALSE`

**Renamed `show` → `event` everywhere**

The `Show` entity was renamed to `Event` for clarity (`Event` = a night at a venue grouping multiple artist `Concert`s).

- Renamed files: `models/show.py` → `event.py`, `models/show_attendee_association.py` → `event_attendee_association.py`, `schemas/show.py` → `event.py`, `crud/show.py` → `event.py`, `routes/show.py` → `event.py`, `repositories/show.py` → `event.py`
- DB tables: `shows` → `events`, `show_attendees` → `event_attendees`
- FK column: `Concert.show_id` → `Concert.event_id`
- Relationships: `.shows` → `.events` on Venue, Festival, Attendee models
- Mock data: `nofx_show/nfg_show` → `nofx_event/nfg_event`, `nofx_show_artists/concerts/attendees` → `nofx_artists/concerts/attendees`
- Fixed typo `asssociated` → `associated` in `crud/venue.py`
- Removed debug `print()` / ANSI color statements from `crud/event.py`
- All error messages updated to say "events" instead of "shows"

---

## Known issues to fix (prioritized)

### HIGH
1. **Route ordering bug** — In every router file, `GET /resource/{id}` is registered before `GET /resource/`, so the list endpoint returns 422 instead of a list. Fix: swap the order so the no-param route is registered first. Affects all 10 routers.

2. **Photo/video create broken** — `EventCreate.concerts` uses `ConcertCreate` which has `photos_ids`/`videos_ids` (lists of existing IDs), but `crud/event.py` `create()` iterates `concert.photos` and `concert.videos` (fields that don't exist on `ConcertCreate`). Photos/videos are silently dropped on event creation. The create and update paths are inconsistent.

### MEDIUM
3. **Double engine creation** — `create_engine()` runs at module level in `database.py` AND again inside `lifespan` in `main.py` (demo mode path). Should reuse the single engine from `database.py`.

4. **`UnboundLocalError` risk** — In `crud/concert.py`, `crud/festival.py`, etc., `new_*` variables are referenced in `except IntegrityError` blocks but may not be assigned if the error occurs before the assignment. Will mask the real error with an `UnboundLocalError`.

5. **`artist update()` ignores `address_id`** — `crud/artist.py` update only sets `name`, silently drops `address_id` changes.

6. **CORS misconfiguration** — `allow_origins=["*"]` + `allow_credentials=True` is spec-invalid. Browsers reject credentialed requests with wildcard origin. Should use explicit origin list.

### LOW
7. **`VenueResponse.name` commented out** — `schemas/venue.py` has `name` and `address_id` commented out, so venue name is never returned in API responses. Likely unintentional.

8. **`ConcertBase.id` in create schema** — `ConcertBase` exposes `id: Optional[int]` which leaks into `ConcertCreate`. IDs should not be in create schemas; the `id` field exists only for the update path inside `EventCreate.concerts`.

9. **Unconditional festival DB query** — `crud/event.py` `create()` queries for festival even when `festival_id` is `None`.

10. **Remaining debug print** — `crud/concert.py` still has `print("CRUD CREATE Concert", concert)` on line 42.
