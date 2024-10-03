from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def read_root():
    return "Welcome to the 'Concerts I Have Been To' API"
