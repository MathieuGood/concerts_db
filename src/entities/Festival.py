from dataclasses import dataclass
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column
from src.entities.Base import Base


@dataclass
class Festival(Base):

    __tablename__ = "festivals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[Date] = mapped_column(nullable=True)
    end_date: Mapped[Date] = mapped_column(nullable=True)
