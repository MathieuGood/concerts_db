from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class AttendeeBase(BaseModel):
    firstname: str
    lastname: Optional[str] = None


class AttendeeCreate(AttendeeBase):
    pass


class AttendeeResponse(AttendeeBase):
    id: int
    events: Optional[List["EventResponse"]] = None

    model_config = ConfigDict(from_attributes=True)


from schemas.event import EventResponse
