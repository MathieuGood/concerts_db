from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.country import Country
from schemas.country import CountryCreate


def get(db: Session, country_id: int) -> Country:
    country = db.query(Country).filter(Country.id == country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail=f"Country with ID {country_id} not found.")
    return country


def get_all(db: Session) -> list[Country]:
    return db.query(Country).order_by(Country.name).all()


def find_or_create(db: Session, name: str) -> Country:
    country = db.query(Country).filter(Country.name.ilike(name.strip())).first()
    if country:
        return country
    new_country = Country(name=name.strip())
    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country


def create(db: Session, country: CountryCreate) -> Country:
    try:
        new_country = Country(name=country.name.strip())
        db.add(new_country)
        db.commit()
        db.refresh(new_country)
        return new_country
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Country '{country.name}' already exists.")


def update(db: Session, country_id: int, country: CountryCreate) -> Country:
    try:
        updated = db.query(Country).filter(Country.id == country_id).first()
        if not updated:
            raise HTTPException(status_code=404, detail=f"Country with ID {country_id} not found.")
        updated.name = country.name.strip()
        db.commit()
        db.refresh(updated)
        return updated
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Country '{country.name}' already exists.")


def delete(db: Session, country_id: int) -> dict:
    country = db.query(Country).filter(Country.id == country_id).first()
    if not country:
        return {"message": f"Country #{country_id} does not exist."}
    if country.cities or country.artists:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete '{country.name}' as it has cities or artists associated with it.",
        )
    try:
        db.delete(country)
        db.commit()
        return {"message": f"Country #{country_id} '{country.name}' deleted."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Cannot delete country '{country.name}'.")
