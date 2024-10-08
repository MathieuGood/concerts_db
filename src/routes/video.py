from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.video import get, get_all, create, update, delete
from database.database import get_db
from schemas.video import VideoCreate

router = APIRouter()


@router.get("/video/{video_id}")
async def get_video(video_id: int, db: Session = Depends(get_db)):
    return get(db, video_id)


@router.get("/video/")
async def get_all_videos(db: Session = Depends(get_db)):
    return get_all(db)


# Create video
@router.post("/video/")
async def create_video(video: VideoCreate, db: Session = Depends(get_db)):
    return create(db, video)


# Update video
@router.put("/video/{video_id}")
async def update_video(
    video_id: int, video: VideoCreate, db: Session = Depends(get_db)
):
    return update(db, video_id, video)


# Delete video
@router.delete("/video/{video_id}")
async def delete_video(video_id: int, db: Session = Depends(get_db)):
    return delete(db, video_id)
