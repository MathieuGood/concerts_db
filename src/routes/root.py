from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db


router = APIRouter()
session = Depends(get_db)


@router.get("/")
async def read_root():
    return "Hello World"
