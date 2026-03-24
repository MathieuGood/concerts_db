from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class FestivalBase(BaseModel):
    name: str


class FestivalCreate(FestivalBase):
    pass


class FestivalResponse(FestivalBase):
    id: int
    events: Optional[List["EventResponse"]] = None

    model_config = ConfigDict(from_attributes=True)


from schemas.event import EventResponse
