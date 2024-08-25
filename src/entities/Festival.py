from dataclasses import dataclass
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from entities.Base import Base


@dataclass
class Festival(Base):
    __tablename__ = "festivals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    shows: Mapped[List["Show"]] = relationship("Show", back_populates="festival")


from entities.Show import Show
