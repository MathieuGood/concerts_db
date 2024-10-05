from typing import Optional
from pydantic import BaseModel, ConfigDict


class VideoBase(BaseModel):
    path: str


class VideoCreate(VideoBase):
    concert_id: int


class VideoResponse(VideoBase):
    id: int
    concert: Optional["ConcertResponse"] = None

    model_config = ConfigDict(from_attributes=True)


from schemas.concert import ConcertResponse
