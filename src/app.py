from sqlalchemy import Engine, create_engine, MetaData, insert, text
from entities.Base import Base
from entities.User import User
from entities.Address import Address
from sqlalchemy.orm import Session

from entities.repositories.PersonRepository import PersonRepository
from mockup_data.characters import characters


def delete_all_users(session: Session):
    session.execute(text("DELETE FROM users"))
    session.execute(text("DELETE FROM addresses"))
    session.commit()


def main():
    # engine: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    import os
    os.remove("../database/concerts_db.sqlite")

    engine: Engine = create_engine(
        "sqlite+pysqlite:///database/concerts_db.sqlite", echo=True
    )
    metadata_obj = MetaData()

    Base.metadata.create_all(engine)

    session = Session(engine)

    # delete_all_users(session)

    user_repository = PersonRepository(session)

    user_repository.add_multiple(characters)

    kenny: User = user_repository.get_by_id(4)
    stan: User = user_repository.get_by_id(3)

    kenny_address = Address(city="South Park", country="USA")
    stan_address = Address(city="Tegridyville", country="USA")
    kenny.addresses.append(kenny_address)
    stan.addresses.append(stan_address)

    print("")
    print(kenny.addresses)
    print("")
    print(stan.addresses)

    session.commit()

    # eric = session.get(User, 1)
    # print(eric.fullname)

    # all_users = user_repository.get_all()

    # for user in all_users:
    #     print(user)


if __name__ == "__main__":
    main()
