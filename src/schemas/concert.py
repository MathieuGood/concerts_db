from pydantic import BaseModel
from typing import List, Optional


class ConcertBase(BaseModel):
    comments: str
    setlist: Optional[str] = None


class ConcertCreate(ConcertBase):
    # show_id not required because it is not known at the time
    # show_id: int
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


from schemas.show import ShowResponse
from schemas.artist import ArtistResponse
from schemas.photo import PhotoResponse
from schemas.video import VideoResponse
