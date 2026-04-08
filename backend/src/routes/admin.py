from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from schemas.user import UserCreate, UserResponse, ResetPasswordRequest
from schemas.response import ApiResponse
from crud import user as user_crud
from crud.user import reset_password
from auth.dependencies import require_admin
from models.user import User

router = APIRouter(prefix="/admin")


@router.get("/users", response_model=ApiResponse[List[UserResponse]])
def list_users(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=user_crud.get_all(db))


@router.post("/users", response_model=ApiResponse[UserResponse])
def create_user(user_in: UserCreate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=user_crud.create(db, user_in))


@router.put("/users/{user_id}/password", response_model=ApiResponse[UserResponse])
def reset_user_password(user_id: int, body: ResetPasswordRequest, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    updated = reset_password(db, user_id, body.new_password)
    return ApiResponse(success=True, data=UserResponse.model_validate(updated))


@router.delete("/users/{user_id}")
def delete_user(user_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    if user_id == current_user.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Cannot delete your own account.")
    result = user_crud.delete(db, user_id)
    return ApiResponse(success=True, data=None, message=result["message"])
