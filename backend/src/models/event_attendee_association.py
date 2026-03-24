from sqlalchemy import Table, Column, ForeignKey
from models.base import Base

event_attendee_association = Table(
    "event_attendees",
    Base.metadata,
    Column("event_id", ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "attendee_id", ForeignKey("attendees.id", ondelete="RESTRICT"), primary_key=True
    ),
)
