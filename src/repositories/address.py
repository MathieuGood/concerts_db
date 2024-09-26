from sqlalchemy.orm import Session
from entities.address import Address
from repositories.base import BaseRepository


class AddressRepository(BaseRepository[Address]):
    def __init__(self, session: Session):
        super().__init__(session, Address)