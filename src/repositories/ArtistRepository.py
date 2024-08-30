from sqlalchemy.orm import Session
from entities.Artist import Artist
from repositories.BaseRepository import BaseRepository


class ArtistRepository(BaseRepository[Artist]):
    def __init__(self, session: Session):
        super().__init__(session, Artist)