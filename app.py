from sqlalchemy import Engine, create_engine, MetaData, insert, text
from sqlalchemy.orm import Session
from src.mockup_data.concerts_mock_data import venues, nofx_show
from src.entities.Base import Base
from src.entities.Person import Person
from src.entities.Artist import Artist
from src.entities.Concert import Concert
from src.entities.Festival import Festival
from src.entities.Address import Address
from src.entities.Venue import Venue
from src.repositories.VenueRepository import VenueRepository
from src.repositories.ConcertRepository import ConcertRepository
from src.repositories.PersonRepository import PersonRepository
from src.repositories.AddressRepository import AddressRepository
from src.repositories.FestivalRepository import FestivalRepository
from src.repositories.PhotoRepository import PhotoRepository
from src.repositories.VideoRepository import VideoRepository
from src.repositories.ShowRepository import ShowRepository


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

    venue_repository = VenueRepository(session)
    show_repository = ShowRepository(session)
    person_repository = PersonRepository(session)

    venue_repository.add_multiple(venues)
    show_repository.add(nofx_show)

    session.commit()

    fillmore: Venue = venue_repository.get_by_id(1)
    red_rocks: Venue = venue_repository.get_by_id(2)

    print("")
    print(fillmore.address)
    print("")
    print(red_rocks.address)

    first_concert = session.get(Concert, 1)
    print(first_concert)


if __name__ == "__main__":
    main()
