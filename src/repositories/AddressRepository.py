from sqlalchemy.orm import Session
from entities.Address import Address
from repositories.BaseRepository import BaseRepository


class AddressRepository(BaseRepository[Address]):
    def __init__(self, session: Session):
        super().__init__(session, Address)