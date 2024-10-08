from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.address import get, get_all, create, update, delete
from database.database import get_db
from schemas.address import AddressCreate

router = APIRouter()


@router.get("/address/{address_id}")
async def get_address(address_id: int, db: Session = Depends(get_db)):
    return get(db, address_id)


@router.get("/address/")
async def get_all_addresss(db: Session = Depends(get_db)):
    return get_all(db)


@router.post("/address/")
async def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    return create(db, address)


@router.put("/address/{address_id}")
async def update_address(
    address_id: int, address: AddressCreate, db: Session = Depends(get_db)
):
    return update(db, address_id, address)


@router.delete("/address/{address_id}")
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    return delete(db, address_id)
