from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.address import get, get_all, create, update, delete
from database.database import get_db
from schemas.AddressSchema import AddressCreate

router = APIRouter()
session = Depends(get_db)

router = APIRouter()


@router.get("/address/{address_id}")
def get_address(address_id: int, db: Session = session):
    return get(db, address_id)


@router.get("/address/")
def get_all_addresss(db: Session = session):
    return get_all(db)


# Create address
@router.post("/address/")
def create_address(address: AddressCreate, db: Session = session):
    return create(db, address)


# Update address
@router.put("/address/{address_id}")
def update_address(address_id: int, address: AddressCreate, db: Session = session):
    return update(db, address_id, address)


# Delete address
@router.delete("/address/{address_id}")
def delete_address(address_id: int, db: Session = session):
    return delete(db, address_id)
