import datetime
from typing import List, Optional

from pydantic import BaseModel

from entities.Address import Address
from entities.Artist import Artist
from entities.Concert import Concert
from entities.Person import Person
from entities.Venue import Venue


laiterie = Venue(
    name="La Laiterie",
    address=Address(
        street="Rue du Hohwald", city="Strasbourg", zip="67100", country="France"
    ),
)

descendents = Artist(name="Descendents", country="USA")
hogwash = Artist(name="Hoghwash", country="France")
franck = Person(firstname="Franck", lastname="Ludwig")

concert = Concert(
    date=datetime.date(2024, 6, 14),
    venue=laiterie,
    artists=[descendents, hogwash],
    attendees=[franck],
)

print(concert.model_dump())


