from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from entities.Address import Address
from schemas.AddressSchema import AddressCreate


def get(db: Session, address_id: int):
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(
            status_code=404, detail=f"Address with ID {address_id} not found."
        )
    return address


def get_all(db: Session):
    return db.query(Address).all()


def create(db: Session, address: AddressCreate) -> Address:
    try:
        db_address = Address(name=address.name)
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Address '{address.name}' already exists."
        )


def update(db: Session, address_id: int, address: AddressCreate) -> Address | HTTPException:
    try:
        db_address: Address | None = db.query(Address).filter(Address.id == address_id).first()
        if db_address is None:
            raise HTTPException(
                status_code=404, detail=f"Address with ID {address_id} not found."
            )
        db_address.name = address.name
        db.commit()
        db.refresh(db_address)
        return db_address
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Address '{address.name}' already exists."
        )


def delete(db: Session, address_id: int) -> dict[str, str] | HTTPException:
    db_address: Address |None = db.query(Address).filter(Address.id == address_id).first()
    if not db_address:
        return {"message": f"Address #{address_id} does not exist."}
    address_name = db_address.name
    db.delete(db_address)
    db.commit()
    return {"message": f"Address #{address_id} '{address_name}' deleted."}
