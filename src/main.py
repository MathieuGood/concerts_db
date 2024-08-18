from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker
from mockup_data.concerts_mock_data import venues, nofx_show, nfg_show, festivals
from database.db_connector import delete_database, get_db_session
from entities.Base import Base
from entities.Person import Person
from entities.Artist import Artist
from entities.Concert import Concert
from entities.Festival import Festival
from entities.Address import Address
from entities.Venue import Venue
from repositories.VenueRepository import VenueRepository
from repositories.ConcertRepository import ConcertRepository
from repositories.PersonRepository import PersonRepository
from repositories.AddressRepository import AddressRepository
from repositories.FestivalRepository import FestivalRepository
from repositories.PhotoRepository import PhotoRepository
from repositories.VideoRepository import VideoRepository
from repositories.ShowRepository import ShowRepository


def main():
    delete_database()
    session = get_db_session()

    venue_repository = VenueRepository(session)
    show_repository = ShowRepository(session)
    person_repository = PersonRepository(session)
    festival_repository = FestivalRepository(session)

    venue_repository.add_multiple(venues)
    festival_repository.add_multiple(festivals)
    show_repository.add(nofx_show)
    show_repository.add(nfg_show)
    session.commit()

    print(venue_repository.get_all())


if __name__ == "__main__":
    main()
