from sqlalchemy.orm import Session
from entities.artist import Artist
from repositories.base import BaseRepository


class ArtistRepository(BaseRepository[Artist]):
    def __init__(self, session: Session):
        super().__init__(session, Artist)

    def get_all(self):
        artists = self.session.query(Artist).all()
        return sorted(artists, key=lambda artist: artist.name)
    