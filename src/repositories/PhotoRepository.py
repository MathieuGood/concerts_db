from sqlalchemy.orm import Session
from entities.Photo import Photo
from repositories.BaseRepository import BaseRepository


class PhotoRepository(BaseRepository[Photo]):
    def __init__(self, session: Session):
        super().__init__(session, Photo)