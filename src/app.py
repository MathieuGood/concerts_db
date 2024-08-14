from flask import Flask
from src.mockup_data.concerts_mock_data import venues, nofx_show
from src.db_session import create_session
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
    session = create_session()

    app = Flask(__name__)

    venue_repository = VenueRepository(session)
    show_repository = ShowRepository(session)
    person_repository = PersonRepository(session)

    venue_repository.add_multiple(venues)
    show_repository.add(nofx_show)
    session.commit()


    first_concert = session.get(Concert, 1)
    print(first_concert)


if __name__ == "__main__":
    main()
