from pydantic import BaseModel, Field
from typing import List, Optional


class AttendeeBase(BaseModel):
    firstname: str
    lastname: Optional[str] = None


class AttendeeCreate(AttendeeBase):
    pass


class AttendeeResponse(AttendeeBase):
    id: int
    shows: Optional[List["ShowResponse"]] = None

    class Config:
        from_attributes = True


from schemas.show import ShowResponse
