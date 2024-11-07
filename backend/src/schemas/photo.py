from typing import Optional
from pydantic import BaseModel, ConfigDict


class PhotoBase(BaseModel):
    path: str


class PhotoCreate(PhotoBase):
    concert_id: int


class PhotoResponse(PhotoBase):
    id: int
    concert: Optional["ConcertResponse"] = None

    model_config = ConfigDict(from_attributes=True)


from schemas.concert import ConcertResponse
