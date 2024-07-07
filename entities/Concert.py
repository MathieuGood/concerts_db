from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from entities.Artist import Artist
from entities.Festival import Festival
from entities.Person import Person
from entities.Venue import Venue


class Concert(BaseModel):
    date: datetime
    venue: Venue
    artists: List[Artist]
    price: Optional[float] = None
    festival = Festival
    attendees: List[Person] = []
