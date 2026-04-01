from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from crud.address import get, get_all, create, update, delete
from database.database import get_db
from schemas.address import AddressCreate, AddressResponse
from schemas.response import ApiResponse

router = APIRouter()


@router.get("/address/", response_model=ApiResponse[List[AddressResponse]])
async def get_all_addresss(db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get_all(db))


@router.get("/address/{address_id}", response_model=ApiResponse[AddressResponse])
async def get_address(address_id: int, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get(db, address_id))


@router.post("/address/", response_model=ApiResponse[AddressResponse])
async def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=create(db, address))


@router.put("/address/{address_id}", response_model=ApiResponse[AddressResponse])
async def update_address(
    address_id: int, address: AddressCreate, db: Session = Depends(get_db)
):
    return ApiResponse(success=True, data=update(db, address_id, address))


@router.delete("/address/{address_id}")
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    result = delete(db, address_id)
    return ApiResponse(success=True, data=None, message=result["message"])
