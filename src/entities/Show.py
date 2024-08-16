from dataclasses import dataclass
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from entities.Base import Base


@dataclass
class Show(Base):
    __tablename__ = "shows"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    event_date: Mapped[date] = mapped_column(nullable=False)
    comments: Mapped[str] = mapped_column(default="", nullable=False)

    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"), nullable=False)
    festival_id: Mapped[int] = mapped_column(ForeignKey("festivals.id"), nullable=True)

    venue: Mapped["Venue"] = relationship("Venue", back_populates="shows")
    festival: Mapped["Festival"] = relationship("Festival", back_populates="shows")

    concerts: Mapped[List["Concert"]] = relationship("Concert", back_populates="show")
    attendees: Mapped[List["Person"]] = relationship(
        "Person", secondary="show_attendees", back_populates="shows"
    )


from entities.Venue import Venue
from entities.Festival import Festival
from entities.Artist import Artist
from entities.Person import Person
from entities.Photo import Photo
from entities.Video import Video
from entities.Concert import Concert
