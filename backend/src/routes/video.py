from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from crud.video import get, get_all, create, update, delete
from database.database import get_db
from schemas.video import VideoCreate, VideoResponse
from schemas.response import ApiResponse

router = APIRouter()


@router.get("/video/", response_model=ApiResponse[List[VideoResponse]])
async def get_all_videos(db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get_all(db))


@router.get("/video/{video_id}", response_model=ApiResponse[VideoResponse])
async def get_video(video_id: int, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=get(db, video_id))


@router.post("/video/", response_model=ApiResponse[VideoResponse])
async def create_video(video: VideoCreate, db: Session = Depends(get_db)):
    return ApiResponse(success=True, data=create(db, video))


@router.put("/video/{video_id}", response_model=ApiResponse[VideoResponse])
async def update_video(
    video_id: int, video: VideoCreate, db: Session = Depends(get_db)
):
    return ApiResponse(success=True, data=update(db, video_id, video))


@router.delete("/video/{video_id}")
async def delete_video(video_id: int, db: Session = Depends(get_db)):
    result = delete(db, video_id)
    return ApiResponse(success=True, data=None, message=result["message"])
