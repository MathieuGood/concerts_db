from sqlalchemy.orm import Session
from entities.photo import Photo
from repositories.base import BaseRepository


class PhotoRepository(BaseRepository[Photo]):
    def __init__(self, session: Session):
        super().__init__(session, Photo)