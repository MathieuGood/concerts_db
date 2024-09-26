from entities.video import Video
from fastapi import HTTPException
from schemas.video import VideoCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get(db: Session, video_id: int):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(
            status_code=404, detail=f"Video with ID {video_id} not found."
        )
    return video


def get_all(db: Session):
    return db.query(Video).all()


def create(db: Session, video: VideoCreate) -> Video:
    try:
        new_video = Video(path=video.path, concert_id=video.concert_id)
        db.add(new_video)
        db.commit()
        db.refresh(new_video)
        return new_video
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Video '{new_video.path}' already exists."
        )


def update(db: Session, video_id: int, video: VideoCreate) -> Video:
    try:
        updated_video: Video = (
            db.query(Video).filter(Video.id == video_id).first()
        )
        if updated_video is None:
            raise HTTPException(
                status_code=404, detail=f"Video with ID {video_id} not found."
            )
        updated_video.path = video.path
        updated_video.concert_id = video.concert_id
        db.commit()
        db.refresh(updated_video)
        return updated_video
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Video '{video.path}' already exists."
        )


def delete(db: Session, video_id: int):
    deleted_video: Video = (
        db.query(Video).filter(Video.id == video_id).first()
    )
    if not deleted_video:
        return {"message": f"Video #{video_id} does not exist."}
    db.delete(deleted_video)
    db.commit()
    return {"message": f"Video #{video_id} '{deleted_video.path}' deleted."}
