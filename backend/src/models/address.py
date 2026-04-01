from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class Address(Base):
    __tablename__ = "addresses"
    __table_args__ = (UniqueConstraint("city", "country", name="_city_country_uc"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
