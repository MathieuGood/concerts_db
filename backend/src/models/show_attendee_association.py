from sqlalchemy import Table, Column, ForeignKey
from models.base import Base

show_attendee_association = Table(
    "show_attendees",
    Base.metadata,
    Column("show_id", ForeignKey("shows.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "attendee_id", ForeignKey("attendees.id", ondelete="RESTRICT"), primary_key=True
    ),
)
