from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.user import LoginRequest, TokenResponse, UserResponse
from schemas.response import ApiResponse
from crud.user import authenticate
from auth.jwt import create_access_token
from auth.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=ApiResponse[TokenResponse])
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate(db, body.email, body.password)
    token = create_access_token(user.id)
    return ApiResponse(
        success=True,
        data=TokenResponse(access_token=token, user=UserResponse.model_validate(user)),
    )


@router.get("/me", response_model=ApiResponse[UserResponse])
def me(current_user: User = Depends(get_current_user)):
    return ApiResponse(success=True, data=UserResponse.model_validate(current_user))
