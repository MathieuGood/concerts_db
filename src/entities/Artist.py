from dataclasses import dataclass
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.entities.Base import Base


@dataclass
class Artist(Base):

    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
