from dataclasses import dataclass
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.Base import Base


@dataclass
class Person(Base):

    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=True)

    shows: Mapped[List["Show"]] = relationship(
        "Show", secondary="show_attendees", back_populates="attendees"
    )


from entities.Show import Show
from entities.ShowPersonAssociation import show_person_association
    