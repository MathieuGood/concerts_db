from dataclasses import dataclass
from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.Base import Base


@dataclass
class Concert(Base):

    __tablename__ = "concerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_date: Mapped[Date] = mapped_column()
    comments: Mapped[str] = mapped_column(String, nullable=True)

    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"), nullable=False)
    festival_id: Mapped[int] = mapped_column(ForeignKey("festivals.id"), nullable=True)

    venue: Mapped["Venue"] = relationship("Venue")
    festival: Mapped["Festival"] = relationship("Festival")
    artists: Mapped["Artist"] = relationship(
        "Artist", secondary="concert_artists", back_populates="concerts"
    )
    attendees: Mapped["Person"] = relationship(
        "Person", secondary="concert_attendees", back_populates="concerts"
    )


from entities.Venue import Venue
from entities.Festival import Festival
from entities.Artist import Artist
from entities.Person import Person
