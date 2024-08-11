from sqlalchemy.orm import Session
from src.repositories.BaseRepository import BaseRepository
from src.entities.Person import Person


class PersonRepository(BaseRepository[Person]):
    def __init__(self, session: Session):
        super().__init__(session, Person)
