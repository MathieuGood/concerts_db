from typing import List
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from models.base import Base


class Show(Base):
    __tablename__ = "shows"
    __table_args__ = (UniqueConstraint("event_date", "venue_id", name="_date_venue_uc"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    event_date: Mapped[date] = mapped_column(nullable=False)
    comments: Mapped[str] = mapped_column(default="", nullable=False)

    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"), nullable=False)
    festival_id: Mapped[int] = mapped_column(ForeignKey("festivals.id"), nullable=True)

    venue: Mapped["Venue"] = relationship("Venue", back_populates="shows")
    festival: Mapped["Festival"] = relationship("Festival", back_populates="shows")

    concerts: Mapped[List["Concert"]] = relationship(
        "Concert", back_populates="show", cascade="all, delete-orphan"
    )
    attendees: Mapped[List["Attendee"]] = relationship(
        "Attendee", secondary="show_attendees", back_populates="shows"
    )


from models.venue import Venue
from models.festival import Festival
from models.attendee import Attendee
from models.concert import Concert
