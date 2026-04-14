# concerts_db — Project Reference

## Deployment

**Live URL:** `https://concerts.mathieubon.com`
**VPS port:** `8082` (nginx → Docker Compose)
**Deploy:** push to `main` → GitHub Actions → SSH into VPS → `git pull` + `docker compose -f docker-compose.prod.yml up -d --build`
**VPS app dir:** `~/apps/concerts_db/`
**SQLite DB on VPS:** `/data/concerts_db.sqlite` (volume-mounted from `~/apps/concerts_db/data/`)

For full deployment procedures and VPS infrastructure details, see:
`/Users/mathieugood/guru_code/vps/CLAUDE.md` and `deploy-docker-app.md`

### GitHub Actions secrets needed (Settings → Secrets → Actions)

| Secret | Value |
|---|---|
| `VPS_SSH_KEY` | contents of `~/.ssh/github_actions_vps` |
| `VPS_HOST` | `51.91.98.35` |
| `VPS_USER` | `ubuntu` |
| `SECRET_KEY` | random string for JWT signing (e.g. `openssl rand -hex 32`) |

### Migration history (one-time scripts, safe to re-run)

```bash
# 1. Add users table + user_id columns + create admin user
docker exec concerts_db-backend-1 uv run python src/scripts/migrate_add_users.py

# 2. Add name column to users, set admin name = 'Mathieu'
docker exec concerts_db-backend-1 uv run python src/scripts/migrate_add_user_name.py
```

Default admin credentials after migration:
- **Email:** `bon.mathieu@gmail.com`
- **Password:** `changeme` ← change immediately via the admin panel at `/admin`

### CSV backup cron (on VPS)

Backups write to `/data/backups/` inside the container (mounted from `~/apps/concerts_db/data/backups/`).
Filename format: `concerts_YYYYMMDD_HHMMSS.csv`

```bash
(crontab -l 2>/dev/null; echo "0 3 * * * docker exec concerts_db-backend-1 uv run python src/scripts/export_csv.py 2>/dev/null") | crontab -
```

### Useful one-off commands

```bash
# Import CSV data
docker exec concerts_db-backend-1 uv run python src/scripts/import_csv.py

# Export DB to CSV (backup)
docker exec concerts_db-backend-1 uv run python src/scripts/export_csv.py
```

---

## How to run locally

```bash
# Backend
cd backend
uv run uvicorn main:app --reload --app-dir src
# → http://127.0.0.1:8000

# Frontend
cd frontend
npm run dev
# → http://localhost:5173 (proxies /api/ to localhost:8000)
```

The SQLite DB (`/data/concerts_db.sqlite`) auto-creates on first startup via `Base.metadata.create_all()` in the lifespan. Locally, set `DATABASE_URI=sqlite+pysqlite:////tmp/concerts_db.sqlite` in `backend/.env`.
To reset with seed data: set `DEMO_MODE=TRUE` in `backend/.env`, restart once, then set back to `FALSE`.

---

## Tech stack

**Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 (ORM), Pydantic v2, SQLite, uvicorn, uv (package manager)
**Auth:** JWT (python-jose, HS256, 7-day tokens), bcrypt for password hashing
**Frontend:** Vue 3 (`<script setup>` + Composition API), TypeScript, Vite 7, Vue Router 4, PrimeVue 4 (Aura preset, violet theme), Tailwind CSS 4, native fetch API

**Old React frontend** preserved in `old_react_frontend/` for reference.

---

## Project structure

```
concerts_db/
├── .github/workflows/deploy.yml      # GitHub Actions: SSH → git pull → docker compose up --build
├── Dockerfile.backend                 # Python 3.12-slim + uv
├── Dockerfile.frontend.prod           # Node 22 build → nginx:alpine
├── docker-compose.prod.yml            # nginx:8082 → backend:8000 (internal); ./data:/data volume
├── frontend/
│   └── nginx.conf                     # Container nginx: /api/ → backend:8000, /* → Vue SPA
├── backend/
│   ├── .env                           # DATABASE_URI + DEMO_MODE + PYTHONPATH + SECRET_KEY (not committed)
│   ├── pyproject.toml                 # uv project config
│   ├── uv.lock
│   └── src/
│       ├── main.py                    # FastAPI app + lifespan + router registration + CORS
│       ├── config.py                  # Config: DATABASE_URI, DEMO_MODE, SECRET_KEY
│       ├── database/
│       │   └── database.py            # engine, SessionLocal, get_db(), seed_data()
│       ├── auth/
│       │   ├── jwt.py                 # create_access_token(user_id), decode_token(token) — HS256, 7 days
│       │   ├── password.py            # hash_password / verify_password using bcrypt directly
│       │   └── dependencies.py        # get_current_user (Bearer token → User), require_admin
│       ├── models/                    # SQLAlchemy ORM models
│       │   ├── base.py
│       │   ├── user.py                # id, email (unique), hashed_password, name (nullable), is_admin, created_at
│       │   ├── address.py             # UNUSED — kept but no relationships
│       │   ├── artist.py              # country_id (nullable FK → countries)
│       │   ├── attendee.py            # user_id FK → users; Unique: (firstname, lastname, user_id)
│       │   ├── city.py                # id, name, country_id FK; UniqueConstraint(name, country_id)
│       │   ├── concert.py
│       │   ├── country.py             # id, name (unique)
│       │   ├── event.py               # user_id FK → users; Unique: (event_date, venue_id, user_id)
│       │   ├── event_attendee_association.py
│       │   ├── festival.py
│       │   ├── photo.py
│       │   ├── venue.py               # city_id FK → cities; UniqueConstraint(name, city_id)
│       │   └── video.py
│       ├── schemas/                   # Pydantic request/response schemas
│       │   ├── user.py                # UserCreate (name?), UserResponse, LoginRequest, TokenResponse,
│       │   │                          # ChangePasswordRequest, ResetPasswordRequest
│       │   ├── artist.py / attendee.py / city.py / concert.py / country.py
│       │   ├── event.py / festival.py / photo.py / venue.py / video.py
│       │   └── response.py            # Generic ApiResponse[T] envelope
│       ├── crud/
│       │   ├── user.py                # get_all, get_by_email, create, authenticate, delete,
│       │   │                          # change_password, reset_password
│       │   ├── artist.py              # joinedload(Artist.country)
│       │   ├── attendee.py            # all ops scoped by user_id
│       │   ├── city.py                # find_or_create(name, country_id)
│       │   ├── concert.py
│       │   ├── country.py             # find_or_create(name) — case-insensitive ilike
│       │   ├── event.py               # all ops scoped by user_id
│       │   ├── festival.py
│       │   ├── photo.py / venue.py / video.py
│       ├── routes/
│       │   ├── auth.py                # POST /auth/login, GET /auth/me, PUT /auth/change-password
│       │   ├── admin.py               # GET/POST/DELETE /admin/users, PUT /admin/users/{id}/password
│       │   ├── root.py
│       │   ├── artist.py / attendee.py / city.py / concert.py / country.py
│       │   ├── event.py / festival.py / photo.py / venue.py / video.py / address.py
│       ├── repositories/              # Thin repository wrappers over BaseRepository
│       └── scripts/
│           ├── import_csv.py          # Import data/concerts_import.csv into DB
│           ├── export_csv.py          # Export DB to CSV (backup format)
│           ├── migrate_add_users.py   # Migration 1: users table + user_id columns
│           └── migrate_add_user_name.py  # Migration 2: name column on users
├── frontend/
│   └── src/
│       ├── main.ts                    # App entry, PrimeVue + ToastService + ConfirmationService
│       ├── App.vue                    # Root layout: AppHeader + ConfirmDialog + router-view + Toast
│       ├── composables/
│       │   └── useAuth.ts             # Shared auth state (user ref, isAdmin, setUser, logout)
│       ├── router/index.ts            # All routes + guards (see Routes section below)
│       ├── models/                    # TypeScript interfaces matching backend schemas
│       ├── services/
│       │   ├── api.ts                 # Base fetch wrapper — injects Bearer token, redirects to /login on 401
│       │   ├── authService.ts         # login, saveSession, clearSession, getStoredUser, isLoggedIn, changePassword
│       │   ├── adminService.ts        # getUsers, createUser, deleteUser, resetUserPassword
│       │   ├── artistService.ts       # getAll, create, update, delete
│       │   ├── attendeeService.ts     # getAll, create, update, delete
│       │   ├── cityService.ts         # getAll, create, update, delete, findOrCreate
│       │   ├── countryService.ts      # getAll, create, update, delete, findOrCreate
│       │   ├── eventService.ts        # getAll, getOne, create, update, delete, buildPayload
│       │   ├── festivalService.ts     # getAll, create, update, delete
│       │   └── venueService.ts        # getAll, create, update, delete
│       ├── components/
│       │   ├── AppHeader.vue          # Full nav bar (see Header section below)
│       │   ├── ConcertRow.vue
│       │   ├── VenueSelectOrCreate.vue / ArtistSelectOrCreate.vue / FestivalSelectOrCreate.vue
│       │   └── AttendeeMultiSelect.vue
│       └── views/
│           ├── LoginView.vue          # Email + password form → POST /auth/login → stores token
│           ├── AdminView.vue          # User list, create, delete, reset password, change own password
│           ├── EventList.vue          # Homepage — sortable DataTable of all events (ASC by date default)
│           ├── EventForm.vue          # Create / edit event (concerts, venue, festival, attendees)
│           ├── LibraryView.vue        # Hub grid linking to all 6 entity pages
│           ├── ArtistsView.vue        # Artists DataTable + stats + expandable event list
│           ├── VenuesView.vue         # Venues DataTable + stats + expandable event list
│           ├── CitiesView.vue         # Cities DataTable + stats + expandable event list
│           ├── CountriesView.vue      # Countries DataTable + stats + expandable event list
│           ├── AttendeesView.vue      # Attendees DataTable + stats + expandable event list
│           └── FestivalsView.vue      # Festivals DataTable + stats + expandable event list
└── old_react_frontend/                # Archived React app (reference only)
```

---

## Routes

| Path | Component | Auth | Notes |
|------|-----------|------|-------|
| `/login` | LoginView | Public | |
| `/` | EventList | Yes | Default sort: date ASC |
| `/event/new` | EventForm | Yes | |
| `/event/:id` | EventForm | Yes | |
| `/library` | LibraryView | Yes | Hub grid of entity links |
| `/artists` | ArtistsView | Yes | |
| `/venues` | VenuesView | Yes | |
| `/cities` | CitiesView | Yes | |
| `/countries` | CountriesView | Yes | |
| `/attendees` | AttendeesView | Yes | |
| `/festivals` | FestivalsView | Yes | |
| `/admin` | AdminView | Admin only | |

---

## AppHeader nav

Left: `🎸 Concerts` logo (→ `/`)

Right (in order):
1. **New Event** button (pi-plus, filled violet)
2. **Shows** icon (pi-calendar) → `/` — highlighted when active
3. **Artists** icon (pi-star) → `/artists` — highlighted when active
4. **Venues** icon (pi-building) → `/venues`
5. **Cities** icon (pi-map-marker) → `/cities`
6. **Countries** icon (pi-globe) → `/countries`
7. **People** icon (pi-users) → `/attendees`
8. **Festivals** icon (pi-ticket) → `/festivals`
9. **Admin** icon (pi-shield) → `/admin` — only if `isAdmin`
10. User name (hidden on mobile)
11. **Sign out** icon (pi-sign-out) — triggers ConfirmDialog
12. **Theme toggle** (pi-moon / pi-sun)

Active icon state: `:text="route.path !== link.path"` — filled when active, ghost otherwise.
Theme: auto-follows system `prefers-color-scheme` if no manual preference saved; otherwise reads `localStorage('theme')`. Listens for OS-level changes.

---

## Entity pages — shared pattern

All 6 entity views (Artists, Venues, Cities, Countries, Attendees, Festivals) follow the same pattern:

**Layout:**
- Search bar + count badge + Add button (with `ml-3` gap before button)
- Inline add form (shown on toggle, hidden by default)
- `size="small"` DataTable with `editMode="row"`, `v-model:editingRows`, expandable rows

**Table columns:** Entity-specific data columns + date columns (first/last) + merged action column

**Merged action column (`width:5.5rem`):**
- Normal mode: pencil icon → calls `startEdit(row)`
- Edit mode: ✓ (success) + ✕ (secondary) + 🗑 (danger) — calls `saveRow(data)`, `cancelEdit(row)`, `onDelete(row)`
- Manual `editingRows` management: `startEdit` pushes row, `cancelEdit`/`saveRow` filter it out

**Expansion panel:** Stat pills (violet count + gray label, rounded-full) then full event list table (clicking any row navigates to `/event/:id`)

**Stats computed client-side** from the full events payload: Sets for unique venue/city/country counts, min/max date for first/last seen.

**Shows column** present on: Venues, Cities, Countries, Attendees (violet count, sortable, `width:75px`)

---

## Authentication

**Model:** JWT, HS256, 7-day tokens stored in `localStorage`.

**Flow:**
1. Unauthenticated → redirected to `/login`
2. POST `/auth/login` → `{access_token, user}` → stored in localStorage
3. All API requests include `Authorization: Bearer <token>`
4. 401 response → token cleared → redirect to `/login`

**Multi-user data isolation:**
- `events.user_id` and `attendees.user_id` — data scoped per user
- Shared tables (artists, venues, cities, countries, festivals) — no user scoping

**Auth & admin endpoints:**

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/login` | No | Returns JWT + user info |
| GET | `/auth/me` | Yes | Returns current user |
| PUT | `/auth/change-password` | Yes | Change own password (requires current password) |
| GET | `/admin/users` | Admin | List all users |
| POST | `/admin/users` | Admin | Create user |
| PUT | `/admin/users/{id}/password` | Admin | Force-reset any user's password |
| DELETE | `/admin/users/{id}` | Admin | Delete user (cannot delete self) |

---

## Data model

### Conceptual summary

An **Event** is a live music night at a **Venue** on a specific date, owned by a **User**. It optionally belongs to a **Festival**. It has one or more **Concerts** (each Concert = one artist performing that night). **Attendees** are people who attended the event (many-to-many, scoped per user). Each **Concert** can have **Photos** and **Videos**.

```
User ──── Event ──── Festival (optional)
            └── Venue ──── City ──── Country
            └── Concert ──── Artist ──── Country (optional)
            │       ├── Photo
            │       └── Video
            └── Attendees (M2M, scoped per user)
```

### DB tables & key fields

| Table | Key columns | Notes |
|-------|-------------|-------|
| `users` | `id`, `email`, `hashed_password`, `name`, `is_admin`, `created_at` | `email` unique; `name` nullable |
| `countries` | `id`, `name` | `name` unique; shared across users |
| `cities` | `id`, `name`, `country_id` | Unique: (name, country_id); shared |
| `artists` | `id`, `name`, `country_id` | `name` unique; `country_id` nullable; shared |
| `venues` | `id`, `name`, `city_id` | Unique: (name, city_id); shared |
| `festivals` | `id`, `name` | `name` unique; shared |
| `events` | `id`, `name`, `event_date`, `comments`, `venue_id`, `festival_id`, `user_id` | Unique: (event_date, venue_id, user_id) |
| `event_attendees` | `event_id`, `attendee_id` | M2M join table |
| `attendees` | `id`, `firstname`, `lastname`, `user_id` | Unique: (firstname, lastname, user_id) |
| `concerts` | `id`, `comments`, `setlist`, `event_id`, `artist_id` | Cascade deleted with event |
| `photos` | `id`, `path`, `concert_id` | Unique: (path, concert_id) |
| `videos` | `id`, `path`, `concert_id` | Unique: (path, concert_id) |

---

## API

### Response envelope

All endpoints return a consistent `ApiResponse` envelope (`schemas/response.py`):

```json
{ "success": true, "data": { ... } }
{ "success": true, "data": null, "message": "Event #3 deleted." }
{ "success": false, "data": null, "message": "Event with ID 3 not found." }
```

### Endpoints (all require Bearer token except auth)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/auth/login` | Login → JWT |
| GET | `/auth/me` | Current user |
| PUT | `/auth/change-password` | Change own password |
| GET/POST/PUT/DELETE | `/admin/users`, `/admin/users/{id}` | User management (admin) |
| GET/POST/PUT/DELETE | `/country/`, `/country/{id}` | Country CRUD (shared) |
| GET/POST/PUT/DELETE | `/city/`, `/city/{id}` | City CRUD; GET supports `?country_id=` filter |
| GET/POST/PUT/DELETE | `/artist/`, `/artist/{id}` | Artist CRUD (shared) |
| GET/POST/PUT/DELETE | `/attendee/`, `/attendee/{id}` | Attendee CRUD (scoped per user) |
| GET/POST/PUT/DELETE | `/concert/`, `/concert/{id}` | Concert CRUD |
| GET/POST/PUT/DELETE | `/event/`, `/event/{id}` | Event CRUD (scoped per user) |
| GET/POST/PUT/DELETE | `/festival/`, `/festival/{id}` | Festival CRUD (shared) |
| GET/POST/PUT/DELETE | `/venue/`, `/venue/{id}` | Venue CRUD (shared) |
| GET/POST/PUT/DELETE | `/photo/`, `/photo/{id}` | Photo CRUD |
| GET/POST/PUT/DELETE | `/video/`, `/video/{id}` | Video CRUD |

### Backend patterns

**Route serialization** — every GET/POST/PUT route must declare `response_model=ApiResponse[XxxResponse]`. DELETE routes are exempt.

**Response schema design** — `XxxResponse` schemas omit back-references to prevent circular serialization. Dependency graph is strictly one-directional.

**Eager loading** — always use `joinedload` for nested relationships in CRUD queries.

**`find_or_create` pattern** — `crud/country.py` and `crud/city.py` have `find_or_create` (case-insensitive ilike). Frontend calls `countryService.findOrCreate` / `cityService.findOrCreate` before creating venues/artists.

**User scoping** — `crud/event.py` and `crud/attendee.py` always filter by `user_id`. The `user_id` is passed from the route via `current_user.id` (from `get_current_user` dependency).

---

## Frontend — key patterns

### Auth flow
- `services/authService.ts` — login, session storage, helpers
- `composables/useAuth.ts` — shared reactive state (user, isAdmin, logout)
- `services/api.ts` — auto-injects `Authorization: Bearer <token>` header; redirects to `/login` on 401
- Router guard in `router/index.ts` — redirects unauthenticated to `/login`; non-admins blocked from `/admin`

### Dark / light theme
- Toggle button in `AppHeader.vue` adds/removes `.dark` class on `<html>`
- Preference saved in `localStorage`; auto-follows system `prefers-color-scheme` if no manual preference set
- Live OS-level change detection via `matchMedia.addEventListener('change', ...)`

### Inline creation (venues, artists, festivals, attendees)
- `SelectOrCreate` components: dropdown + `+` button → inline mini-form
- Venue: `countryService.findOrCreate` → `cityService.findOrCreate` → `venueService.create`

### Row editing (entity pages)
- `editMode="row"` on DataTable; `editingRows` managed manually (no `:rowEditor="true"` column)
- `startEdit(row)` pushes to `editingRows`; `cancelEdit` / `saveRow` filter it out
- `saveRow(data)` calls the entity's `onSave({ newData: data })` then removes from `editingRows`
- Delete only accessible in edit mode (shown in merged action column's `#editor` slot)

---

## Importing data from concert tickets (CSV workflow)

### CSV format
File: `concerts_db/data/concerts_import.csv`

**One row = one event.** Multiple artists and attendees are semicolon-separated.

```
event_date,venue,city,country,artists,attendees,festival,comments
2003-05-27,Salle des Fêtes,Schiltigheim,France,Jean-Louis Aubert,,,
2011-04-15,Zénith Europe,Strasbourg,France,NOFX;Dropkick Murphys;Sick of It All,,,
```

**~98 events imported** into the deployed database (as of 2026-04-06), assigned to admin user.

---

## Known issues / TODO

- **Photos/videos** — backend supports them, frontend does not yet.
- **No pagination** on list endpoints — fine for personal use.
- **`models/address.py`** — unused, safe to delete.
- **World map / city heatmap** — planned feature: add `latitude`/`longitude` to `cities` table, geocode via Nominatim, render bubble map with Leaflet.
- **Automated backups** — daily CSV export cron exists on VPS; delivery to Synology NAS or email not yet implemented.
