from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.video import get, get_all, create, update, delete
from database.database import get_db
from schemas.VideoSchema import VideoCreate

router = APIRouter()
session = Depends(get_db)

router = APIRouter()


@router.get("/video/{video_id}")
def get_video(video_id: int, db: Session = session):
    return get(db, video_id)


@router.get("/video/")
def get_all_videos(db: Session = session):
    return get_all(db)


# Create video
@router.post("/video/")
def create_video(video: VideoCreate, db: Session = session):
    return create(db, video)


# Update video
@router.put("/video/{video_id}")
def update_video(video_id: int, video: VideoCreate, db: Session = session):
    return update(db, video_id, video)


# Delete video
@router.delete("/video/{video_id}")
def delete_video(video_id: int, db: Session = session):
    return delete(db, video_id)
