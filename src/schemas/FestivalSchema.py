from pydantic import BaseModel
from typing import List, Optional


class FestivalBase(BaseModel):
    name: str


class FestivalCreate(FestivalBase):
    pass


class FestivalResponse(FestivalBase):
    id: int
    shows: Optional[List["ShowResponse"]] = None

    class Config:
        from_attributes = True


from schemas.ShowSchema import ShowResponse
