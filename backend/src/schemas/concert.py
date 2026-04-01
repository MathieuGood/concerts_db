from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from schemas.artist import ArtistResponse
from schemas.photo import PhotoResponse
from schemas.video import VideoResponse


class ConcertBase(BaseModel):
    comments: str
    setlist: Optional[str] = None


class ConcertCreate(ConcertBase):
    id: Optional[int] = None
    event_id: Optional[int] = None
    artist_id: int
    photos_ids: Optional[List[int]] = None
    videos_ids: Optional[List[int]] = None


class ConcertResponse(ConcertBase):
    id: int
    comments: Optional[str] = None
    setlist: Optional[str] = None
    event_id: int
    artist_id: int
    artist: Optional[ArtistResponse] = None
    photos: Optional[List[PhotoResponse]] = None
    videos: Optional[List[VideoResponse]] = None

    model_config = ConfigDict(from_attributes=True)
