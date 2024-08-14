from flask import Flask
from mockup_data.concerts_mock_data import venues, nofx_show
from db_session import create_session
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
