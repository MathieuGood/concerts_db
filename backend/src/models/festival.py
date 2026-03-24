from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class Festival(Base):
    __tablename__ = "festivals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    events: Mapped[List["Event"]] = relationship("Event", back_populates="festival")


from models.event import Event
