from pydantic import BaseModel, ConfigDict
from typing import Optional
from schemas.artist import ArtistResponse, ArtistListResponse


class ConcertBase(BaseModel):
    comments: str
    setlist: Optional[str] = None
    i_played: bool = False


class ConcertCreate(ConcertBase):
    id: Optional[int] = None
    event_id: Optional[int] = None
    artist_id: int


class ConcertResponse(ConcertBase):
    id: int
    comments: Optional[str] = None
    event_id: int
    artist_id: int
    artist: Optional[ArtistResponse] = None

    model_config = ConfigDict(from_attributes=True)


class ConcertListResponse(ConcertBase):
    """Lightweight concert for list — omits artist.country."""
    id: int
    event_id: int
    artist_id: int
    artist: Optional[ArtistListResponse] = None

    model_config = ConfigDict(from_attributes=True)
