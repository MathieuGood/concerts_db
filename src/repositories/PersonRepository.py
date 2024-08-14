from sqlalchemy.orm import Session
from repositories.BaseRepository import BaseRepository
from entities.Person import Person


class PersonRepository(BaseRepository[Person]):
    def __init__(self, session: Session):
        super().__init__(session, Person)
