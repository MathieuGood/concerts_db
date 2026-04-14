from typing import List, Optional
from sqlalchemy import Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class Festival(Base):
    __tablename__ = "festivals"
    __table_args__ = (UniqueConstraint("name", "year", name="uq_festival_name_year"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    events: Mapped[List["Event"]] = relationship("Event", back_populates="festival")


from models.event import Event
