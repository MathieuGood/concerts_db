from sqlalchemy import Engine, create_engine, MetaData, insert, text
from entities.Base import Base
from entities.Person import Person
from entities.Artist import Artist
from entities.Concert import Concert
from entities.Festival import Festival
from entities.Address import Address
from sqlalchemy.orm import Session
from entities.Venue import Venue
from mockup_data.venues import venues
from entities.repositories.VenueRepository import VenueRepository


def delete_all_users(session: Session):
    session.execute(text("DELETE FROM users"))
    session.execute(text("DELETE FROM addresses"))
    session.commit()


def main():
    # engine: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    import os

    try:
        os.remove("database/concerts_db.sqlite")
        print("*** Database file removed ***")
    except FileNotFoundError as e:
        print(e)

        pass

    engine: Engine = create_engine(
        "sqlite+pysqlite:///database/concerts_db.sqlite", echo=True
    )
    metadata_obj = MetaData()

    Base.metadata.create_all(engine)

    session = Session(engine)

    # delete_all_users(session)

    venue_repository = VenueRepository(session)

    venue_repository.add_multiple(venues)

    fillmore: Venue = venue_repository.get_by_id(1)
    red_rocks: Venue = venue_repository.get_by_id(2)

    print("")
    print(fillmore.address)
    print("")
    print(red_rocks.address)

    session.commit()

    # eric = session.get(User, 1)
    # print(eric.fullname)

    # all_users = user_repository.get_all()

    # for user in all_users:
    #     print(user)


if __name__ == "__main__":
    main()
