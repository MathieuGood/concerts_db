from typing import List
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.base import Base

class Attendee(Base):
    __tablename__ = "attendees"
    __table_args__ = (
        UniqueConstraint("firstname", "lastname", name="_firstname_lastname_uc"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=True)

    shows: Mapped[List["Show"]] = relationship(
        "Show", secondary="show_attendees", back_populates="attendees"
    )


from entities.show import Show
from entities.show_attendee_association import show_attendee_association
