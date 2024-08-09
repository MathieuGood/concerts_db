from typing import List
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, user) -> None:
        self.session.add(user)
        self.session.commit()

    def add_multiple(self, users: List[User]) -> None:
        self.session.add_all(users)
        self.session.commit()

    def get_by_id(self, id) -> User:
        return self.session.get(User, id)

    def get_all(self) -> List[User]:
        return self.session.query(User).all()

    def delete(self, id) -> None:
        user = self.get(id)
        self.session.delete(user)
        self.session.commit()


from entities.User import User
