from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.address import Address
from schemas.address import AddressCreate


def get(db: Session, address_id: int) -> Address:
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(
            status_code=404, detail=f"Address with ID {address_id} not found."
        )
    return address


def get_all(db: Session) -> list[Address]:
    return db.query(Address).all()


def create(db: Session, address: AddressCreate) -> Address:
    try:
        new_address = Address(city=address.city, country=address.country)
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        return new_address
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Address '{address.city}, {address.country}' already exists.",
        )


def update(
    db: Session, address_id: int, address: AddressCreate
) -> Address | HTTPException:
    try:
        updated_address: Address | None = (
            db.query(Address).filter(Address.id == address_id).first()
        )
        if updated_address is None:
            raise HTTPException(
                status_code=404, detail=f"Address with ID {address_id} not found."
            )
        updated_address.city = address.city
        updated_address.country = address.country
        db.commit()
        db.refresh(updated_address)
        return updated_address
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Address '{address.city}, {address.country}' already exists.",
        )


def delete(db: Session, address_id: int) -> dict[str, str] | HTTPException:
    deleted_address: Address | None = (
        db.query(Address).filter(Address.id == address_id).first()
    )

    if not deleted_address:
        return {"message": f"Address #{address_id} does not exist."}
    address = f"{deleted_address.city}, {deleted_address.country}"

    if deleted_address.venues or deleted_address.artists:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete address '{address}' as it is associated with one or more venues or artists",
        )

    try:
        db.delete(deleted_address)
        db.commit()
        return {"message": f"Address #{address_id} '{address}' deleted."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete address '{address}', it is still associated with one or more venues.",
        )
