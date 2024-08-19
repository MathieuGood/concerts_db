from pydantic import BaseModel, Field
from typing import List, Optional


class FestivalBase(BaseModel):
    name: str


class FestivalCreate(FestivalBase):
    pass


class FestivalResponse(FestivalBase):
    id: int
    shows: Optional[List["ShowResponse"]] = Field(None, exclude=True)

    class Config:
        from_attributes = True


from schemas.ShowSchema import ShowResponse
