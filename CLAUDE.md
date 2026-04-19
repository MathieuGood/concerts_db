# concerts_db — Reference

## Deploy

- **URL:** `https://concerts.mathieubon.com` · **VPS port:** 8082 (nginx → Docker Compose)
- **Deploy:** push `main` → GH Actions → SSH VPS → `git fetch origin && git checkout main && git reset --hard origin/main` + `docker compose -f docker-compose.prod.yml up -d --build`
- **VPS dir:** `~/apps/concerts_db/` · **DB:** `/data/concerts_db.sqlite` (volume `./data:/data`)
- **GH secrets:** `VPS_SSH_KEY`, `VPS_HOST=51.91.98.35`, `VPS_USER=ubuntu`, `SECRET_KEY` (JWT signing, `openssl rand -hex 32`)
- **Infra docs:** `/Users/mathieugood/guru_code/vps/CLAUDE.md`
- **Admin login:** `bon.mathieu@gmail.com` / (password changed via `/admin`)

### One-off commands (VPS)
```bash
# Import/export CSV
docker exec concerts_db-backend-1 uv run python src/scripts/import_csv.py
docker exec concerts_db-backend-1 uv run python src/scripts/export_csv.py
# Daily backup cron (installed): 03:00 export to ~/apps/concerts_db/backups/
```

## Local run

```bash
cd backend && uv run uvicorn main:app --reload --app-dir src   # :8000
cd frontend && npm run dev                                      # :5173, proxies /api/ → :8000
```

`backend/.env`: `DATABASE_URI=sqlite+pysqlite:////tmp/concerts_db.sqlite`, `SECRET_KEY=...` required.

### Dev seed automatique (`dataset/`)

Activer avec `DEV=true` dans `backend/.env` (déjà présent en local).  
Placer un CSV d'export dans `dataset/` à la racine (gitignored).  
À chaque démarrage du backend : **reset complet de la DB** + import du CSV le plus récent.  
Compte admin créé automatiquement : `dev@dev.com` / `dev`

```bash
# Exporter depuis la prod puis déposer dans dataset/
scp ubuntu@51.91.98.35:~/apps/concerts_db/backups/<fichier>.csv dataset/
```

`DEV` absent ou `DEV=false` → no-op. Le `.env` prod sur le VPS ne contient pas `DEV=true`.

## Tech stack

- **Backend:** Python 3.12, FastAPI (`root_path="/api"` for Swagger behind nginx), SQLAlchemy 2.0, Pydantic v2, SQLite, uv
- **Auth:** JWT HS256 7-day tokens (python-jose), bcrypt
- **Frontend:** Vue 3 `<script setup>`, TypeScript, Vite 7, Vue Router 4, PrimeVue 4 (Aura/violet), Tailwind 4, fetch API

## Project structure (essentials)

```
backend/src/
├── main.py              # FastAPI + lifespan + routers + CORS (root_path="/api")
├── config.py            # DATABASE_URI, SECRET_KEY
├── database/database.py # engine, SessionLocal, get_db
├── auth/
│   ├── jwt.py           # create_access_token, decode_token
│   ├── password.py      # bcrypt hash/verify
│   └── dependencies.py  # get_current_user, get_optional_user, require_admin
├── models/              # user, country, city, artist, venue, festival, event, concert, attendee, event_attendee_association, photo, video
├── schemas/             # Pydantic; EventResponse includes user_id
├── crud/                # user-scoped: event.py, attendee.py; shared: others
├── routes/              # one per entity + auth, admin, transfer, root
└── scripts/             # import_csv, export_csv

frontend/src/
├── main.ts / App.vue
├── composables/useAuth.ts, useListState.ts
├── router/index.ts      # meta.public | requiresAuth | adminOnly
├── services/            # api.ts (Bearer + 401 redirect), authService, adminService, *Service
├── components/          # AppHeader, *SelectOrCreate, AttendeeMultiSelect, ConcertRow
└── views/               # LoginView, EventList, EventForm, AdminView, LibraryView,
                         # ArtistsView, VenuesView, CitiesView, CountriesView,
                         # AttendeesView, FestivalsView, StatsView, ImportView
```

## Routes

| Path | View | Access |
|---|---|---|
| `/login` | LoginView | public |
| `/` | EventList | **public read** |
| `/event/:id` | EventForm | **public read**; edit if owner or admin |
| `/event/new` | EventForm | auth |
| `/library`, `/artists`, `/venues`, `/cities`, `/countries`, `/festivals`, `/stats` | *ListView | **public read** |
| `/attendees` | AttendeesView | auth (user-scoped) |
| `/admin`, `/import` | Admin/Import | admin |

Router guard in `router/index.ts`: `public` → allow; else require auth; `adminOnly` → require `is_admin`.

## Authentication & authorization

- **JWT** in `localStorage`. `services/api.ts` auto-injects `Authorization: Bearer`, clears session + redirects on 401.
- **Read access:** GET on events + shared entities (artists/venues/cities/countries/festivals/concerts) is **public**. GET `/attendee/` requires auth and is user-scoped.
- **Write access:** POST/PUT/DELETE require auth.
- **Per-user scoping:** `events.user_id`, `attendees.user_id`.
  - Events are **visible to all** but only editable/deletable by owner or admin.
  - Attendees are strictly **private per-user**.
- **Ownership checks in CRUD:**
  - `crud/event.py create`/`update`: attendees validated to belong to current user (403 otherwise).
  - `crud/event.py update`: concerts scoped to `Concert.event_id == event_id` to prevent hijacking.
  - `crud/event.py update`/`delete`: event filtered by `user_id` so only owner can mutate.

### Frontend gating

- `EventForm.vue` / `EventList.vue`: `canEdit = isAdmin || event.user_id === user.id`.
- `EventForm.vue`: if `?edit=true` in URL but not `canEdit`, forces back to view mode after loading.
- `AppHeader.vue`: sign-out button hidden when `!user`.
- Unauthenticated browsing skips attendee fetch in `EventForm.onMounted`.

### Auth & admin endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/auth/login` | — | Returns JWT + user |
| GET | `/auth/me` | yes | Current user |
| PUT | `/auth/change-password` | yes | Change own pwd |
| GET/POST | `/admin/users` | admin | List/create |
| PUT | `/admin/users/{id}/password` | admin | Force reset |
| DELETE | `/admin/users/{id}` | admin | (cannot delete self) |

## Data model

```
User ── Event ── Festival (optional, shared)
         ├── Venue ── City ── Country
         ├── Concert ── Artist ── Country (optional, shared)
         │      ├── Photo
         │      └── Video
         └── Attendees (M2M, private per user)
```

| Table | Key columns | Notes |
|---|---|---|
| `users` | id, email, hashed_password, name, is_admin, created_at | email unique |
| `countries` | id, name | unique; shared |
| `cities` | id, name, country_id | unique (name, country_id); shared |
| `artists` | id, name, country_id | name unique; country nullable; shared |
| `venues` | id, name, city_id | unique (name, city_id); shared |
| `festivals` | id, name, year | name unique; shared |
| `events` | id, name, event_date, comments, venue_id, festival_id, user_id | unique (event_date, venue_id, user_id) |
| `event_attendees` | event_id, attendee_id | M2M |
| `attendees` | id, firstname, lastname, user_id | unique (firstname, lastname, user_id) |
| `concerts` | id, comments, setlist, i_played, event_id, artist_id | cascade with event |
| `photos`, `videos` | id, path, concert_id | unique (path, concert_id) |

## API

**Response envelope** (`schemas/response.py`): `{ success, data, message? }`. Every GET/POST/PUT declares `response_model=ApiResponse[XxxResponse]`. DELETE exempt.

**Schemas:** `XxxResponse` omits back-refs to avoid circular serialization. `EventResponse` includes `user_id` (for frontend edit-gating).

**Patterns:**
- Use `joinedload` for nested relationships in CRUD.
- `find_or_create` on country + city (case-insensitive). Frontend calls `countryService.findOrCreate` → `cityService.findOrCreate` → `venueService.create`.
- Routes for user-scoped entities pass `current_user.id` from `get_current_user` dependency.

## Key patterns

- **Dark theme:** `AppHeader` toggles `.dark` on `<html>`, saves to `localStorage`, live-follows `prefers-color-scheme`.
- **Inline creation:** `VenueSelectOrCreate` / `ArtistSelectOrCreate` / `FestivalSelectOrCreate` / `AttendeeMultiSelect`. For `InputNumber` inside flex rows, use `input-class="!w-full"` (fixes Year field overflow on festival create).
- **Row editing on entity pages:** `editMode="row"` + manual `editingRows` mgmt, merged action column with pencil/save/cancel/delete.
- **Entity pages:** search + count + Add + inline add form + small DataTable + expandable rows (stat pills + events list).
- **Mobile event card:** date inline with artist name (row 1); venue — city on row 2 spanning full width; festival badge on row 3.
- **Accent-insensitive search:** `frontend/src/utils/search.ts` exports `normalize(s)` (NFD decompose + strip diacritics + lowercase). Used in `VenueSelectOrCreate`, `ArtistSelectOrCreate`, and `EventList` search.
- **Infinite scroll (EventList):** all events loaded from API once, rendered 30 at a time via `displayedEvents = filtered.slice(0, displayCount)`. `IntersectionObserver` on a sentinel `<div>` increments `displayCount` by 30. `watch(filtered, ..., { flush: 'sync' })` resets count on filter change.

## CSV import

`concerts_db/data/concerts_import.csv` — one row per event, `artists` and `attendees` semicolon-separated.
```
event_date,venue,city,country,artists,attendees,festival,comments
```
~98 events imported (admin user) as of 2026-04-06.

## Known gaps

- No pagination on entity pages (ArtistsView, VenuesView, etc.) — EventList uses infinite scroll.
- `models/address.py` unused.
- World map / city heatmap: planned (add lat/lng, geocode Nominatim, Leaflet).
- Automated backups: VPS cron exists; email/NAS delivery not implemented.
