from pydantic import BaseModel

from entities.Address import Address


class Venue(BaseModel):
    name: str
    address: Address = None
