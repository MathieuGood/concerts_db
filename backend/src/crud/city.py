from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from models.city import City
from schemas.city import CityCreate


def _with_country(db: Session, city_id: int) -> City:
    return db.query(City).options(joinedload(City.country)).filter(City.id == city_id).first()


def get(db: Session, city_id: int) -> City:
    city = _with_country(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail=f"City with ID {city_id} not found.")
    return city


def get_all(db: Session, country_id: int | None = None) -> list[City]:
    q = db.query(City).options(joinedload(City.country))
    if country_id is not None:
        q = q.filter(City.country_id == country_id)
    return q.order_by(City.name).all()


def find_or_create(db: Session, name: str, country_id: int) -> City:
    city = (
        db.query(City)
        .options(joinedload(City.country))
        .filter(City.name.ilike(name.strip()), City.country_id == country_id)
        .first()
    )
    if city:
        return city
    new_city = City(name=name.strip(), country_id=country_id)
    db.add(new_city)
    db.commit()
    return _with_country(db, new_city.id)


def create(db: Session, city: CityCreate) -> City:
    try:
        new_city = City(name=city.name.strip(), country_id=city.country_id)
        db.add(new_city)
        db.commit()
        return _with_country(db, new_city.id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"City '{city.name}' already exists in this country."
        )


def update(db: Session, city_id: int, city: CityCreate) -> City:
    try:
        updated = db.query(City).filter(City.id == city_id).first()
        if not updated:
            raise HTTPException(status_code=404, detail=f"City with ID {city_id} not found.")
        updated.name = city.name.strip()
        updated.country_id = city.country_id
        db.commit()
        return _with_country(db, updated.id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"City '{city.name}' already exists in this country."
        )


def delete(db: Session, city_id: int) -> dict:
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        return {"message": f"City #{city_id} does not exist."}
    if city.venues:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete '{city.name}' as it has venues associated with it.",
        )
    try:
        db.delete(city)
        db.commit()
        return {"message": f"City #{city_id} '{city.name}' deleted."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Cannot delete city '{city.name}'.")
