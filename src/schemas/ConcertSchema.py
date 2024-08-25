from pydantic import BaseModel, Field
from typing import List, Optional


class ConcertBase(BaseModel):
    comments: str
    setlist: Optional[str] = None


class ConcertCreate(ConcertBase):
    show_id: int
    artist_id: int


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

    class Config:
        from_attributes = True


from schemas.ShowSchema import ShowResponse
from schemas.ArtistSchema import ArtistResponse
from schemas.PhotoSchema import PhotoResponse
from schemas.VideoSchema import VideoResponse
