from typing import List, Type, Generic, TypeVar
from sqlalchemy.orm import Session

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, entity_class: Type[T]):
        self.session = session
        self.entity_class = entity_class

    def add(self, entity: T) -> None:
        self.session.add(entity)
        self.session.commit()

    def add_multiple(self, entities: List[T]) -> None:
        self.session.add_all(entities)
        self.session.commit()

    def get_by_id(self, id) -> T | None:
        return self.session.get(self.entity_class, id)

    def get_all(self) -> List[T]:
        return self.session.query(self.entity_class).all()

    def delete(self, id) -> None:
        entity = self.get_by_id(id)
        if entity:
            self.session.delete(entity)
            self.session.commit()