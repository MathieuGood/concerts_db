from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class ConcertBase(BaseModel):
    comments: str
    setlist: Optional[str] = None


class ConcertCreate(ConcertBase):
    show_id: Optional[int] = None
    artist_id: int
    photos: Optional[List[str]] = None
    videos: Optional[List[str]] = None


class ConcertResponse(ConcertBase):
    id: int
    comments: Optional[str] = None
    setlist: Optional[str] = None
    show_id: int
    artist_id: int
    show: Optional["ShowResponse"] = None
    artist: Optional["ArtistResponse"] = None
    photos: Optional[List["PhotoResponse"]] = None
    videos: Optional[List["VideoResponse"]] = None

    model_config = ConfigDict(from_attributes=True)


from schemas.show import ShowResponse
from schemas.artist import ArtistResponse
from schemas.photo import PhotoResponse
from schemas.video import VideoResponse
