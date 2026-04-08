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

### After deploying auth for the first time (one-time migration)

```bash
# Run migration on VPS to add users table + user_id columns + create admin
docker exec concerts_db-backend-1 uv run python src/scripts/migrate_add_users.py
```

Default admin credentials after migration:
- **Email:** `bon.mathieu@gmail.com`
- **Password:** `changeme` ← change immediately via the admin panel at `/admin`

### CSV backup cron (on VPS)

```bash
(crontab -l 2>/dev/null; echo "0 3 * * * docker exec concerts_db-backend-1 uv run python src/scripts/export_csv.py > /home/ubuntu/apps/concerts_db/backups/backup_\$(date +\%Y\%m\%d).csv 2>/dev/null") | crontab -
```

### Useful one-off commands

```bash
# Import CSV data (run after first deploy or migration)
docker exec concerts_db-backend-1 uv run python src/scripts/import_csv.py

# Export DB to CSV (backup)
docker exec concerts_db-backend-1 uv run python src/scripts/export_csv.py

# Run migration (adds users, user_id columns — safe to run multiple times)
docker exec concerts_db-backend-1 uv run python src/scripts/migrate_add_users.py
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
│       │   ├── __init__.py
│       │   ├── jwt.py                 # create_access_token(user_id), decode_token(token) — HS256, 7 days
│       │   ├── password.py            # hash_password / verify_password using bcrypt directly
│       │   └── dependencies.py        # get_current_user (Bearer token → User), require_admin
│       ├── models/                    # SQLAlchemy ORM models
│       │   ├── base.py
│       │   ├── user.py                # id, email (unique), hashed_password, is_admin, created_at
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
│       │   ├── user.py                # UserCreate, UserResponse, LoginRequest, TokenResponse
│       │   ├── artist.py / attendee.py / city.py / concert.py / country.py
│       │   ├── event.py / festival.py / photo.py / venue.py / video.py
│       │   └── response.py            # Generic ApiResponse[T] envelope
│       ├── crud/                      # Business logic / DB operations
│       │   ├── user.py                # get_all, get_by_email, create, authenticate, delete
│       │   ├── artist.py              # joinedload(Artist.country)
│       │   ├── attendee.py            # all ops scoped by user_id
│       │   ├── city.py                # find_or_create(name, country_id)
│       │   ├── concert.py
│       │   ├── country.py             # find_or_create(name) — case-insensitive ilike
│       │   ├── event.py               # all ops scoped by user_id
│       │   ├── festival.py
│       │   ├── photo.py
│       │   ├── venue.py
│       │   └── video.py
│       ├── routes/                    # FastAPI routers
│       │   ├── auth.py                # POST /auth/login, GET /auth/me
│       │   ├── admin.py               # GET/POST/DELETE /admin/users (admin only)
│       │   ├── root.py
│       │   ├── artist.py / attendee.py / city.py / concert.py / country.py
│       │   ├── event.py / festival.py / photo.py / venue.py / video.py
│       │   └── address.py
│       ├── repositories/              # Thin repository wrappers over BaseRepository
│       └── scripts/
│           ├── import_csv.py          # Import data/concerts_import.csv into DB
│           ├── export_csv.py          # Export DB to CSV (backup format)
│           └── migrate_add_users.py   # One-time migration: add users table + user_id columns
├── frontend/
│   └── src/
│       ├── main.ts                    # App entry, PrimeVue + ToastService setup
│       ├── App.vue                    # Root layout: AppHeader + router-view + Toast
│       ├── composables/
│       │   └── useAuth.ts             # Shared auth state (user ref, isAdmin, setUser, logout)
│       ├── router/index.ts            # Routes + guards: /login (public), /, /event/new, /event/:id, /admin
│       ├── models/                    # TypeScript interfaces matching backend schemas
│       ├── services/
│       │   ├── api.ts                 # Base fetch wrapper — injects Bearer token, redirects to /login on 401
│       │   ├── authService.ts         # login(), saveSession(), clearSession(), getStoredUser(), isLoggedIn()
│       │   ├── adminService.ts        # getUsers(), createUser(), deleteUser() — calls /admin/* endpoints
│       │   ├── eventService.ts / attendeeService.ts / venueService.ts / artistService.ts / etc.
│       ├── components/
│       │   ├── AppHeader.vue          # Nav + user email + sign-out + admin icon + dark/light toggle
│       │   ├── ConcertRow.vue
│       │   ├── VenueSelectOrCreate.vue / ArtistSelectOrCreate.vue / FestivalSelectOrCreate.vue
│       │   └── AttendeeMultiSelect.vue
│       └── views/
│           ├── LoginView.vue          # Email + password form → POST /auth/login → stores token
│           ├── AdminView.vue          # List users, create user, delete user (admin only, /admin)
│           ├── EventList.vue
│           └── EventForm.vue
└── old_react_frontend/                # Archived React app (reference only)
```

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
- Admin can manage users at `/admin`

**Auth endpoints:**

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/login` | No | Returns JWT + user info |
| GET | `/auth/me` | Yes | Returns current user |
| GET | `/admin/users` | Admin | List all users |
| POST | `/admin/users` | Admin | Create user |
| DELETE | `/admin/users/{id}` | Admin | Delete user |

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
| GET/POST/DELETE | `/admin/users`, `/admin/users/{id}` | User management (admin) |
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
- Preference saved in `localStorage`

### Inline creation (venues, artists, festivals, attendees)
- `SelectOrCreate` components: dropdown + `+` button → inline mini-form
- Venue: `countryService.findOrCreate` → `cityService.findOrCreate` → `venueService.create`

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

**98 events already imported** into the deployed database (as of 2026-04-06), assigned to admin user.

### Festival tickets — pending (resume later)

Festival day passes don't list individual artists. Workflow: look up full lineup → user selects attended sets → add to CSV.

Pending festivals to process (see previous CLAUDE.md version for full list).

---

## Known issues / TODO

- **Photos/videos** — backend supports them, frontend does not yet.
- **No pagination** on list endpoints — fine for personal use.
- **`models/address.py`** — unused, safe to delete.
- **Admin password change UI** — implemented: "Change my password" section in `/admin` (requires current password); admin can also force-reset any user's password via the key icon per user row.
