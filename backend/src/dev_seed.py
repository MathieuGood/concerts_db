"""
Dev seed: si DEV=true dans backend/.env, réinitialise la DB au démarrage
et importe le CSV le plus récent depuis dataset/ à la racine du projet.

Déclenché à chaque démarrage du backend (lifespan FastAPI).
DEV non défini ou DEV=false → no-op, comportement prod inchangé.

Compte admin créé automatiquement : dev@dev.com / dev
"""
import os
from pathlib import Path

from auth.password import hash_password
from database.database import SessionLocal, engine
from models.base import Base
from models.user import User
from scripts.import_csv import import_csv

# dataset/ est à la racine du projet, 3 niveaux au-dessus de src/
DATASET_DIR = Path(__file__).parents[2] / "dataset"
DEV_EMAIL = "dev@dev.com"
DEV_PASSWORD = "dev"


def _latest_csv(directory: Path) -> Path | None:
    csvs = list(directory.glob("*.csv"))
    return max(csvs, key=lambda p: p.stat().st_mtime) if csvs else None


def seed_if_requested() -> None:
    if os.getenv("DEV", "").lower() != "true":
        return

    if not DATASET_DIR.is_dir():
        print(f"[dev_seed] DEV=true mais dataset/ introuvable ({DATASET_DIR}) — skip")
        return

    csv_path = _latest_csv(DATASET_DIR)
    if csv_path is None:
        print(f"[dev_seed] DEV=true mais aucun CSV dans dataset/ — skip")
        return

    print(f"[dev_seed] dataset/ détecté → réinitialisation DB depuis {csv_path.name}")

    # Reset complet de la DB
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Création du compte admin dev
    db = SessionLocal()
    try:
        user = User(
            email=DEV_EMAIL,
            hashed_password=hash_password(DEV_PASSWORD),
            name="Dev",
            is_admin=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        user_id = user.id
        print(f"[dev_seed] Admin créé : {DEV_EMAIL} / {DEV_PASSWORD}")
    finally:
        db.close()

    import_csv(csv_path, user_id=user_id)
    print(f"[dev_seed] Seed terminé.")
