# concerts_db — Reference

## Deploy

- **URL:** `https://concerts.mathieubon.com` · **VPS port:** 8082 (nginx → Docker Compose)
- **Deploy:** push `main` → GH Actions → SSH VPS → `git pull` + `docker compose -f docker-compose.prod.yml up -d --build`
- **VPS dir:** `~/apps/concerts_db/` · **DB:** `/data/concerts_db.sqlite` (volume `./data:/data`)
- **GH secrets:** `VPS_SSH_KEY`, `VPS_HOST=51.91.98.35`, `VPS_USER=ubuntu`, `SECRET_KEY` (JWT signing, `openssl rand -hex 32`)
- **Infra docs:** `/Users/mathieugood/guru_code/vps/CLAUDE.md`
- **Admin login:** `bon.mathieu@gmail.com` / (password changed via `/admin`)

### One-off commands (VPS)
```bash
# Import/export CSV
docker exec concerts_db-backend-1 uv run python src/scripts/import_csv.py
docker exec concerts_db-backend-1 uv run python src/scripts/export_csv.py
# Migrations (idempotent)
docker exec concerts_db-backend-1 uv run python src/scripts/migrate_add_users.py
docker exec concerts_db-backend-1 uv run python src/scripts/migrate_add_user_name.py
# Daily backup cron (installed): 03:00 export to ~/apps/concerts_db/backups/
```

## Local run

```bash
cd backend && uv run uvicorn main:app --reload --app-dir src   # :8000
cd frontend && npm run dev                                      # :5173, proxies /api/ → :8000
```

`backend/.env`: `DATABASE_URI=sqlite+pysqlite:////tmp/concerts_db.sqlite`, `DEMO_MODE=TRUE` to seed. `SECRET_KEY=...` required.

## Tech stack

- **Backend:** Python 3.12, FastAPI (`root_path="/api"` for Swagger behind nginx), SQLAlchemy 2.0, Pydantic v2, SQLite, uv
- **Auth:** JWT HS256 7-day tokens (python-jose), bcrypt
- **Frontend:** Vue 3 `<script setup>`, TypeScript, Vite 7, Vue Router 4, PrimeVue 4 (Aura/violet), Tailwind 4, fetch API
- Old React app preserved in `old_react_frontend/`

## Project structure (essentials)

```
backend/src/
├── main.py              # FastAPI + lifespan + routers + CORS (root_path="/api")
├── config.py            # DATABASE_URI, DEMO_MODE, SECRET_KEY
├── database/database.py # engine, SessionLocal, get_db, seed_data
├── auth/
│   ├── jwt.py           # create_access_token, decode_token
│   ├── password.py      # bcrypt hash/verify
│   └── dependencies.py  # get_current_user, get_optional_user, require_admin
├── models/              # user, country, city, artist, venue, festival, event, concert, attendee, event_attendee_association, photo, video
├── schemas/             # Pydantic; EventResponse includes user_id
├── crud/                # user-scoped: event.py, attendee.py; shared: others
├── routes/              # one per entity + auth, admin, transfer, root
└── scripts/             # import_csv, export_csv, migrate_*

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

## CSV import

`concerts_db/data/concerts_import.csv` — one row per event, `artists` and `attendees` semicolon-separated.
```
event_date,venue,city,country,artists,attendees,festival,comments
```
~98 events imported (admin user) as of 2026-04-06.

## Known gaps

- Photos/videos: backend-only (no frontend UI).
- No pagination.
- `models/address.py` unused.
- World map / city heatmap: planned (add lat/lng, geocode Nominatim, Leaflet).
- Automated backups: VPS cron exists; email/NAS delivery not implemented.

---

# Textual TUI frontend (planned — `frontend-cli/`)

**Goal:** keyboard-driven alternative to the Vue front for fast data entry. Reuses the existing REST API (same auth flow).

## Stack
Python 3.12 + `uv` · `textual` · `httpx` (async) · `platformdirs` (token storage at `~/.config/concerts-cli/`).

## Planned structure
```
frontend-cli/src/
├── main.py                # Textual App entry
├── config.py              # API_URL via env (local vs prod)
├── api/                   # client.py (httpx + Bearer + 401), auth, events, artists, venues, cities, countries, festivals, attendees
├── models.py              # dataclasses mirroring backend schemas
├── screens/               # login, events_list, event_form, artists, venues, cities, countries, festivals, attendees, stats
└── widgets/               # select_or_create (filter + create modal), date_input (YYYY-MM-DD), nav_header
```

## Phases
1. **Foundations (MVP read):** scaffold, API client + token, login screen, app shell with tabs, events list (DataTable + search).
2. **Event CRUD:** event detail, create/edit form (date, venue+festival select-or-create, dynamic concerts with artist/setlist/i_played, attendees multiselect), delete with confirm.
3. **Entities:** CRUD inline for Artists/Venues/Cities/Countries/Festivals/Attendees.
4. **Polish:** stats, admin (optional), full keyboard shortcuts (`n`, `e`, `d`, `/`, `?`, `q`), config `CONCERTS_API_URL`.

## Open questions (answer before starting)
1. API target: prod only / local only / both via env var?
2. Initial scope: MVP (phases 1+2) or full parity?
3. Admin included?
4. Packaging: `uv run` vs `pipx install`?

## Constraints to remember
- No native combobox in Textual → build `select_or_create` as Input + filtered ListView + modal.
- No native multiselect → checkboxes in ListView.
- No date picker → plain `Input` with `YYYY-MM-DD` validation.
- Attendee fetch requires auth (as on Vue).
