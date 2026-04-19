from typing import List
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from models.base import Base


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (UniqueConstraint("event_date", "venue_id", "user_id", name="_date_venue_user_uc"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    event_date: Mapped[date] = mapped_column(nullable=False)
    comments: Mapped[str] = mapped_column(default="", nullable=False)

    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"), nullable=False, index=True)
    festival_id: Mapped[int] = mapped_column(ForeignKey("festivals.id"), nullable=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)

    venue: Mapped["Venue"] = relationship("Venue", back_populates="events")
    festival: Mapped["Festival"] = relationship("Festival", back_populates="events")

    concerts: Mapped[List["Concert"]] = relationship(
        "Concert", back_populates="event", cascade="all, delete-orphan"
    )
    attendees: Mapped[List["Attendee"]] = relationship(
        "Attendee", secondary="event_attendees", back_populates="events"
    )


from models.venue import Venue
from models.festival import Festival
from models.attendee import Attendee
from models.concert import Concert
