"""
Dev seed: si un répertoire `dataset/` existe à la racine du projet,
réinitialise la DB et importe le CSV le plus récent de ce répertoire.

Déclenché à chaque démarrage du backend (lifespan FastAPI).
Sans `dataset/` → no-op, comportement prod inchangé.

Compte admin créé automatiquement : dev@dev.com / dev
"""
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
    if not DATASET_DIR.is_dir():
        return

    csv_path = _latest_csv(DATASET_DIR)
    if csv_path is None:
        print(f"[dev_seed] dataset/ trouvé mais aucun CSV dedans — skip")
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
