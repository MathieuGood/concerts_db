from sqlalchemy.orm import Session
from entities.Video import Video
from repositories.BaseRepository import BaseRepository


class VideoRepository(BaseRepository[Video]):
    def __init__(self, session: Session):
        super().__init__(session, Video)