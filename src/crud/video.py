from entities.Video import Video
from fastapi import HTTPException
from schemas.VideoSchema import VideoCreate
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
        db_video = Video(name=video.name)
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
        return db_video
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Video '{db_video.name}' already exists."
        )


def update(db: Session, video_id: int, video: VideoCreate) -> Video:
    try:
        db_video: Video = (
            db.query(Video).filter(Video.id == video_id).first()
        )
        if db_video is None:
            raise HTTPException(
                status_code=404, detail=f"Video with ID {video_id} not found."
            )
        db_video.name = video.name
        db.commit()
        db.refresh(db_video)
        return db_video
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Video '{video.name}' already exists."
        )


def delete(db: Session, video_id: int):
    db_video: Video = (
        db.query(Video).filter(Video.id == video_id).first()
    )
    if not db_video:
        return {"message": f"Video #{video_id} does not exist."}
    video_name = db_video.name
    db.delete(db_video)
    db.commit()
    return {"message": f"Video #{video_id} '{video_name}' deleted."}
