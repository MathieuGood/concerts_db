# Concerts DB

A personal app to log every concert I've been to — artists, venues, setlists, festivals, who I went with.

Live at [concerts.mathieubon.com](https://concerts.mathieubon.com). Browsing is open to all, writing requires a login.

## Stack

- **Backend** — FastAPI, SQLAlchemy 2.0, SQLite, JWT auth
- **Frontend** — Vue 3 + TypeScript, PrimeVue, Tailwind

## Run locally

### Docker (recommended)

```bash
# Build and start containers (backend + frontend)
docker compose up --build

# Stop and remove containers
docker compose down -v
```

### Manually starting up backend and frontend servers

For this option, you need to have `uv` and `npm` installed on your machine.

```bash
# backend → http://localhost:8000
cd backend && uv run uvicorn main:app --reload --app-dir src

# frontend → http://localhost:5173 (proxies /api → :8000)
cd frontend && npm install && npm run dev
```

`backend/.env` needs at minimum:

```
DATABASE_URI=sqlite+pysqlite:////tmp/concerts_db.sqlite
SECRET_KEY=<openssl rand -hex 32>
```

### Seeding dev with a prod CSV snapshot

Drop exported CSVs into any directory and point the backend at it:

```
DEV_SEED_CSV_DIR=/absolute/path/to/csv_directory
```

On startup, if the `events` table is empty, the backend imports the **most recent** `*.csv` (by mtime) from that directory. Once seeded, the hook is a no-op — delete the SQLite file to re-seed.

## What's in it

- Events list with search, mobile cards / desktop table
- Event form with artist / venue / festival type-ahead + inline create
- Library views for artists, venues, cities, countries, festivals
- Per-user private attendees
- Stats: histograms and counts
- Admin panel: user management
- CSV import / export
