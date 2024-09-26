from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from entities.base import Base


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
    attendees: Mapped[List["Attendee"]] = relationship(
        "Attendee", secondary="show_attendees", back_populates="shows"
    )


from entities.venue import Venue
from entities.festival import Festival
from entities.attendee import Attendee
from entities.concert import Concert
