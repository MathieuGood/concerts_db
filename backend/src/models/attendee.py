from typing import List
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class Attendee(Base):
    __tablename__ = "attendees"
    __table_args__ = (
        UniqueConstraint("firstname", "lastname", "user_id", name="_firstname_lastname_user_uc"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    events: Mapped[List["Event"]] = relationship(
        "Event", secondary="event_attendees", back_populates="attendees"
    )


from models.event import Event
from models.event_attendee_association import event_attendee_association
