# concerts_db — Project Reference

## How to run

```bash
# Backend
cd backend
uv run uvicorn main:app --reload --app-dir src
# → http://127.0.0.1:8000

# Frontend
cd frontend
npm run dev
# → http://localhost:5173
```

The SQLite DB (`backend/flask_concerts_db.sqlite`) auto-creates on first startup via `Base.metadata.create_all()` in the lifespan.
To reset with seed data: set `DEMO_MODE=TRUE` in `backend/.env`, restart once, then set back to `FALSE`.

---

## Tech stack

**Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 (ORM), Pydantic v2, SQLite (dev) / PostgreSQL (prod), uvicorn, uv (package manager)

**Frontend:** Vue 3 (`<script setup>` + Composition API), TypeScript, Vite 7, Vue Router 4, PrimeVue 4 (Aura preset, violet theme), Tailwind CSS 4, native fetch API

**Old React frontend** preserved in `old_react_frontend/` for reference.

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
│       ├── main.py                   # FastAPI app + lifespan + router registration + exception handler
│       ├── config.py                 # Config class reading .env
│       ├── database/
│       │   └── database.py           # engine, SessionLocal, get_db(), seed_data()
│       ├── models/                   # SQLAlchemy ORM models
│       │   ├── base.py
│       │   ├── address.py            # UNUSED — kept but no relationships; replaced by country/city
│       │   ├── artist.py             # country_id (nullable FK → countries)
│       │   ├── attendee.py
│       │   ├── city.py               # id, name, country_id FK; UniqueConstraint(name, country_id)
│       │   ├── concert.py
│       │   ├── country.py            # id, name (unique)
│       │   ├── event.py
│       │   ├── event_attendee_association.py
│       │   ├── festival.py
│       │   ├── photo.py
│       │   ├── venue.py              # city_id FK → cities; UniqueConstraint(name, city_id)
│       │   └── video.py
│       ├── schemas/                  # Pydantic request/response schemas
│       │   ├── artist.py
│       │   ├── attendee.py
│       │   ├── city.py               # CityCreate, CityResponse (includes country: CountryResponse)
│       │   ├── concert.py
│       │   ├── country.py            # CountryCreate, CountryResponse
│       │   ├── event.py
│       │   ├── festival.py
│       │   ├── photo.py
│       │   ├── response.py           # Generic ApiResponse[T] envelope
│       │   ├── venue.py              # VenueCreate(city_id), VenueResponse (includes city: CityResponse)
│       │   └── video.py
│       ├── crud/                     # Business logic / DB operations
│       │   ├── artist.py             # joinedload(Artist.country)
│       │   ├── attendee.py
│       │   ├── city.py               # find_or_create(name, country_id); _with_country helper
│       │   ├── concert.py
│       │   ├── country.py            # find_or_create(name) — case-insensitive ilike
│       │   ├── event.py              # joinedload chain: venue→city→country, concerts→artist→country
│       │   ├── festival.py
│       │   ├── photo.py
│       │   ├── venue.py              # joinedload(Venue.city).joinedload(City.country)
│       │   └── video.py
│       ├── routes/                   # FastAPI routers
│       │   ├── root.py
│       │   ├── artist.py
│       │   ├── attendee.py
│       │   ├── city.py               # GET ?country_id= filter supported
│       │   ├── concert.py
│       │   ├── country.py
│       │   ├── event.py
│       │   ├── festival.py
│       │   ├── photo.py
│       │   ├── venue.py
│       │   └── video.py
│       ├── repositories/             # Thin repository wrappers over BaseRepository
│       │   ├── base.py
│       │   └── artist.py / attendee.py / concert.py / event.py / festival.py / photo.py / venue.py / video.py
│       └── mockup_data/
│           └── concerts_mock_data.py # Seed data using Country/City/Venue (updated)
├── frontend/                         # Vue 3 frontend
│   ├── src/
│   │   ├── main.ts                   # App entry, PrimeVue + ToastService setup
│   │   ├── App.vue                   # Root layout: AppHeader + router-view + Toast
│   │   ├── assets/styles.css         # Tailwind 4 import + dark mode variant
│   │   ├── router/index.ts           # Routes: / | /event/new | /event/:id
│   │   ├── models/                   # TypeScript interfaces matching backend schemas
│   │   │   ├── Event.ts              # Event, ConcertFormData, EventFormData
│   │   │   ├── Concert.ts
│   │   │   ├── Artist.ts             # country_id?: number | null; country?: Country | null
│   │   │   ├── Venue.ts              # city_id: number; city?: City
│   │   │   ├── City.ts               # id, name, country_id, country: Country
│   │   │   ├── Country.ts            # id, name
│   │   │   ├── Festival.ts
│   │   │   ├── Attendee.ts
│   │   │   └── Address.ts            # UNUSED — kept for reference
│   │   ├── services/                 # Fetch-based API wrappers
│   │   │   ├── api.ts                # Base fetch wrapper (handles ApiResponse envelope)
│   │   │   ├── eventService.ts       # getAll, getOne, create, update, delete + buildPayload
│   │   │   ├── venueService.ts       # getAll, create(name, city_id)
│   │   │   ├── artistService.ts      # getAll, create(name, country_id?)
│   │   │   ├── festivalService.ts
│   │   │   ├── attendeeService.ts    # getAll, create(firstname, lastname?)
│   │   │   ├── countryService.ts     # getAll, create, findOrCreate(name)
│   │   │   └── cityService.ts        # getAll(country_id?), create, findOrCreate(name, country_id)
│   │   ├── components/
│   │   │   ├── AppHeader.vue         # Nav + New Event button + dark/light toggle
│   │   │   ├── ConcertRow.vue        # One concert block (artist + comments + setlist)
│   │   │   ├── VenueSelectOrCreate.vue    # Select existing + inline create: name + country AutoComplete + city AutoComplete
│   │   │   ├── ArtistSelectOrCreate.vue   # Select existing + inline create: name + country AutoComplete (optional)
│   │   │   ├── FestivalSelectOrCreate.vue # Select existing + inline create: name only
│   │   │   └── AttendeeMultiSelect.vue    # MultiSelect + inline create: firstname + lastname (optional)
│   │   └── views/
│   │       ├── EventList.vue         # Search + cards (mobile) / DataTable (desktop); uses venue.city.name
│   │       └── EventForm.vue         # Create & edit; handles venue-created, artist-created, attendee-created events
└── old_react_frontend/               # Archived React app (reference only)
```

---

## Data model

### Conceptual summary

An **Event** is a live music night at a **Venue** on a specific date. It optionally belongs to a **Festival**. It has one or more **Concerts** (each Concert = one artist performing that night). **Attendees** are people who attended the event (many-to-many). Each **Concert** can have **Photos** and **Videos**.

```
Country ──── City ──── Venue
   └── Artist             └── Event ──── Festival (optional)
          └── Concert ◄──── Event
                  ├── Photo     └── Attendees (M2M)
                  └── Video
```

### DB tables & key fields

| Table | Key columns | Notes |
|-------|-------------|-------|
| `countries` | `id`, `name` | `name` unique |
| `cities` | `id`, `name`, `country_id` | Unique: (name, country_id) |
| `artists` | `id`, `name`, `country_id` | `name` unique; `country_id` nullable |
| `venues` | `id`, `name`, `city_id` | Unique: (name, city_id) |
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
| Country | City | 1:Many |
| Country | Artist | 1:Many (optional — artist.country_id nullable) |
| City | Venue | 1:Many |
| Venue | Event | 1:Many |
| Festival | Event | 1:Many (optional FK) |
| Event | Concert | 1:Many (cascade delete) |
| Event | Attendee | Many:Many via `event_attendees` |
| Artist | Concert | 1:Many |
| Concert | Photo | 1:Many (cascade delete) |
| Concert | Video | 1:Many (cascade delete) |

---

## API

### Response envelope

All endpoints return a consistent `ApiResponse` envelope (`schemas/response.py`):

```json
{ "success": true, "data": { ... } }            // GET / POST / PUT
{ "success": true, "data": null, "message": "Event #3 deleted." }  // DELETE
{ "success": false, "data": null, "message": "Event with ID 3 not found." }  // errors
```

The frontend `services/api.ts` unwraps `data` automatically. Errors throw with `message`.

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET/POST/PUT/DELETE | `/country/`, `/country/{id}` | Country CRUD |
| GET/POST/PUT/DELETE | `/city/`, `/city/{id}` | City CRUD; GET supports `?country_id=` filter |
| GET/POST/PUT/DELETE | `/artist/`, `/artist/{id}` | Artist CRUD |
| GET/POST/PUT/DELETE | `/attendee/`, `/attendee/{id}` | Attendee CRUD |
| GET/POST/PUT/DELETE | `/concert/`, `/concert/{id}` | Concert CRUD |
| GET/POST/PUT/DELETE | `/event/`, `/event/{id}` | Event CRUD |
| GET/POST/PUT/DELETE | `/festival/`, `/festival/{id}` | Festival CRUD |
| GET/POST/PUT/DELETE | `/venue/`, `/venue/{id}` | Venue CRUD |
| GET/POST/PUT/DELETE | `/photo/`, `/photo/{id}` | Photo CRUD |
| GET/POST/PUT/DELETE | `/video/`, `/video/{id}` | Video CRUD |

### Backend patterns

**Route serialization** — every GET/POST/PUT route must declare `response_model=ApiResponse[XxxResponse]` on the decorator. Without it FastAPI cannot serialize SQLAlchemy ORM objects through Pydantic's generic `ApiResponse[T]` and returns a 500. DELETE routes are exempt (they always return `data=null`).

**Response schema design** — `XxxResponse` schemas intentionally omit back-references to prevent circular serialization. The dependency graph is strictly one-directional:

```
CountryResponse
  ↑ used by CityResponse, ArtistResponse
      ↑ CityResponse used by VenueResponse
          ↑ VenueResponse used by EventResponse
              ↑ EventResponse contains ConcertResponse → ArtistResponse
```

Never add back-references (e.g. no `country.cities`, `city.venues`, `venue.events`, `artist.concerts`, `concert.event`).

**Eager loading** — always use `joinedload` for nested relationships in CRUD queries. The event query loads the full chain: `Event.venue → Venue.city → City.country` and `Event.concerts → Concert.artist → Artist.country`.

**`find_or_create` pattern** — `crud/country.py` and `crud/city.py` both have `find_or_create` functions (case-insensitive ilike match). The frontend calls `countryService.findOrCreate` / `cityService.findOrCreate` before creating venues/artists to reuse existing location records.

Adding a new route: follow the pattern in any existing route file — import the `XxxResponse` schema, add `response_model=ApiResponse[XxxResponse]` (or `ApiResponse[List[XxxResponse]]`), and never return raw ORM objects without a `response_model`.

### Key schema shapes

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

For event updates, concerts that already exist pass their `id`; new concerts pass `id: null`.

---

## Frontend — key patterns

### Dark / light theme
- Toggle button in `AppHeader.vue` adds/removes `.dark` class on `<html>`
- Preference saved in `localStorage`
- PrimeVue configured with `darkModeSelector: '.dark'`
- Tailwind 4 configured with `@custom-variant dark (&:where(.dark, .dark *))` in `styles.css`

### Inline creation (venues, artists, festivals, attendees)
- Each `SelectOrCreate` component shows a dropdown/multiselect + a `+` button
- The `+` button reveals an inline mini-form
- On save, the new record is POSTed, added to the parent's list, and auto-selected
- Venue creation: `countryService.findOrCreate` → `cityService.findOrCreate` → `venueService.create(name, city_id)`
- Artist creation: optional `countryService.findOrCreate` → `artistService.create(name, country_id?)`
- Attendee creation: `attendeeService.create(firstname, lastname?)` — emits `attendee-created` for parent to push to list

### Country/City AutoComplete
- `VenueSelectOrCreate` and `ArtistSelectOrCreate` use PrimeVue `AutoComplete` (not `InputText`) for location fields
- Countries loaded once on form open; cities loaded lazily when a country is selected
- Free-text allowed (no `force-selection`) — if the typed value doesn't match an existing record, `findOrCreate` creates it on save
- `selectedCountry` / `selectedCity` can be a `Country`/`City` object (selected from dropdown) or a plain string (typed by user) — both cases handled via helper functions that extract `.name`

### EventForm (create + edit)
- Same component for `/event/new` and `/event/:id`
- On mount: fetches venues, festivals, artists, attendees in parallel
- For edit: loads existing event and populates form (concerts keep their `id` for the update path)
- Validation: date required, venue required, ≥1 concert, all concerts have an artist
- Concerts section: add/remove freely; setlist collapsible per concert
- Attendees section: collapsible (hidden by default unless already populated); supports inline creation

---

## Importing data from concert tickets (CSV workflow)

### Overview
Concert tickets are photographed and stored in `~/Desktop/concert_tickets/`. Claude reads them with vision and produces a CSV to import later when the app is stable.

### CSV format
File: `concerts_db/data/concerts_import.csv`

**One row = one event.** Multiple artists and attendees are semicolon-separated within their column.

```
event_date,venue,city,country,artists,attendees,festival,comments
2003-05-27,Salle des Fêtes,Schiltigheim,France,Jean-Louis Aubert,,,
2011-04-15,Zénith Europe,Strasbourg,France,NOFX;Dropkick Murphys;Sick of It All,,,
2008-11-06,Boston College,Boston,USA,RJD2,Saskia Stephens,,"Dining hall show on campus"
2009-06-27,Val de Ville,Neuve-Église,France,Asian Dub Foundation;Cold War Kids,,Festival Décibulles,
```

Column rules:
- `event_date`: ISO 8601 (YYYY-MM-DD)
- `venue`: name only, no street address
- `artists`: semicolon-separated list, proper casing (no ALL CAPS). Maps to one Concert per artist in the DB.
- `attendees`: semicolon-separated `Firstname Lastname`. Creates Attendee records and links them to the event.
- `festival`: festival name if the event is part of one. Will be find-or-created in the festivals table.
- `comments`: free text, quoted if it contains commas.

Import logic (to implement):
1. For each row: `find_or_create` country → city → venue
2. `find_or_create` festival if set
3. Create event (date, venue, festival)
4. For each artist in `artists`: `find_or_create` artist → create Concert linked to event
5. For each attendee in `attendees`: `find_or_create` attendee (split on space: firstname + lastname) → link to event

Non-concerts (sports, cinema, clubbing passes, etc.) are excluded from the CSV.

⚠️ **TODO — Review des billets à faire** : les données du CSV ont été extraites automatiquement par vision IA depuis les photos. Une review manuelle billet par billet a été commencée (2/144 validés) mais n'est pas terminée. Avant d'importer ce CSV en production, reprendre la review avec : *"on reprend la review des billets"* — Claude affichera chaque billet dans le browser avec les données importées côte à côte.

### Festival tickets — special workflow (TODO, resume later)

Festival day/weekend passes don't list individual artists. The workflow to handle them:

1. **Identify the festival** — name, year, location (from the ticket or memory)
2. **Look up the full lineup** — ask Claude: *"Quel était le lineup complet du [Festival] [année] ? Liste tous les artistes avec leur date et heure de passage si possible."*
3. **User selects** — from the full lineup, choose which artists/sets were actually attended
4. **Add to CSV** — one row per selected artist with correct date

Festivals identified from tickets but not yet processed (lineup lookup pending):
- **Punk Rock Holiday 2018** — Tolmin, Slovenia (ticket: `312FBDA0`, `2018-08-07`)
- **Au Grès du Jazz 2009** — La Petite Pierre, France (`073B92A8`, `2009-08-16`)
- **Festival Cabaret Vert** — Charleville-Mézières, France (`0853FCD9`, dates: 21-23 Aug 2015)
- **Rock Am Ring 2008** — Germany (`0C5BE033`)
- **Lez'Arts Scéniques 2006** — Neuve-Église, France (`2FF92A16`, 04-06 Aug 2006)
- **Lez'Arts Scéniques 2010** — Sélestat, France (tickets `7B23635B`, `76A62B58`, 30 Jul – 01 Aug 2010)
- **Hellfest 2006** — Clisson, France (`63748B53`, `2006-06-23`)
- **Dour Festival 2011** — Dour, Belgium (`4CEB4F69`, `2011-07-14`)
- **Rock am See 2007** — Konstanz, Germany (`8192F447`, `2007-09-01`)
- **Les Eurockéennes de Belfort 2012** — Belfort, France (`825F3D51`, `2012-07-01`)
- **Festival Décibulles 2015** — Neuve-Église, France (`AD12408C`)
- **Rock en Seine 2014** — Paris, France (`F04AA405`)
- **Dour Festival** — Dour, Belgium (`CD3F8F7E`)
- **Balelec 2013** — Lausanne, Switzerland (`4513115B`, `2013-05-03`) — partial lineup extracted
- **Earthquake Fest** — Molodoi, date incomplete (`C4CDC69B`)
- **Festival Interférences** — date/year incomplete (`C61C82D0`)
- **Festival Décibulles 2009** — Neuve-Église (`29082F7E`, `2009-06-27`) — some artists extracted, verify full attendance
- **Hard Rock Session 2016** — Colmar, France (`4823EADA`, `2016-08-10`) — some artists extracted, verify

---

## Known issues / TODO

- **CORS origins for production** — `allow_origins` in `main.py` is currently `["http://localhost:5173"]`. Must be updated to include the production frontend URL before deploying. ⚠️ TODO on deploy.
- **Photos/videos** — backend supports them, frontend does not yet. Left for a future iteration.
- **No pagination** on list endpoints — fine for a personal tracker, revisit if data grows.
- **`models/address.py`** — still in codebase but unused (no relationships, no route). Safe to delete once confirmed nothing references it.
