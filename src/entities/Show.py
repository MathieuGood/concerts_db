from dataclasses import dataclass
from typing import List
from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from src.entities.Base import Base


@dataclass
class Show(Base):

    __tablename__ = "shows"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    event_date: Mapped[date] = mapped_column(nullable=False)
    comments: Mapped[str] = mapped_column(nullable=True)

    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"), nullable=False)
    festival_id: Mapped[int] = mapped_column(ForeignKey("festivals.id"), nullable=True)

    venue: Mapped["Venue"] = relationship("Venue", back_populates="shows")
    festival: Mapped["Festival"] = relationship("Festival", back_populates="shows")

    concerts: Mapped[List["Concert"]] = relationship("Concert", back_populates="show")
    attendees: Mapped[List["Person"]] = relationship(
        "Person", secondary="show_attendees", back_populates="shows"
    )


from src.entities.Venue import Venue
from src.entities.Festival import Festival
from src.entities.Artist import Artist
from src.entities.Person import Person
from src.entities.Photo import Photo
from src.entities.Video import Video
from src.entities.Concert import Concert
