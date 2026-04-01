from pydantic import BaseModel, ConfigDict
from typing import Optional


class AttendeeBase(BaseModel):
    firstname: str
    lastname: Optional[str] = None


class AttendeeCreate(AttendeeBase):
    pass


class AttendeeResponse(AttendeeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
