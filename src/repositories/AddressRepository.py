from sqlalchemy.orm import Session
from src.entities.Address import Address
from src.repositories.BaseRepository import BaseRepository


class AddressRepository(BaseRepository[Address]):
    def __init__(self, session: Session):
        super().__init__(session, Address)