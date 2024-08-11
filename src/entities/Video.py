from dataclasses import dataclass
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from entities.Base import Base


@dataclass
class Video(Base):

    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True)
    path : Mapped[str] = mapped_column(String, nullable=False)
