from sqlalchemy.orm import Session
from entities.video import Video
from repositories.base import BaseRepository


class VideoRepository(BaseRepository[Video]):
    def __init__(self, session: Session):
        super().__init__(session, Video)