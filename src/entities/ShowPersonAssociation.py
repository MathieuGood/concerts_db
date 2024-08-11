from sqlalchemy import Table, Column, Integer, ForeignKey
from src.entities.Base import Base


show_person_association = Table(
    "show_attendees",
    Base.metadata,
    Column("show_id", ForeignKey("shows.id"), primary_key=True),
    Column("person_id", ForeignKey("persons.id"), primary_key=True),
)
