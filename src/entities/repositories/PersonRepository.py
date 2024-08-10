from typing import List, Type
from sqlalchemy.orm import Session
from entities.Person import Person


class PersonRepository():
    def __init__(self, session: Session):
        self.session = session

    def add(self, user) -> None:
        self.session.add(user)
        self.session.commit()

    def add_multiple(self, users: List[Person]) -> None:
        self.session.add_all(users)
        self.session.commit()

    def get_by_id(self, id) -> Type[Person] | None:
        return self.session.get(Person, id)

    def get_all(self) -> List[Person]:
        return self.session.query(Person).all()

    def delete(self, id) -> None:
        user = self.get_by_id(id)
        self.session.delete(user)
        self.session.commit()
