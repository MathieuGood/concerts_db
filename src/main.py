from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from mockup_data.concerts_mock_data import venues, nofx_show, nfg_show
from config import Config
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


def delete_database() -> None:
    import os

    try:
        os.remove("src/instance/flask_concerts_db.sqlite")
        print("*** Database file removed ***")
    except FileNotFoundError as e:
        print(e)
        pass

    print("")
    print(os.getcwd())
    print("")
    # input("Press Enter to continue...")


def create_app(db: SQLAlchemy) -> Flask:
    app = Flask(__name__, template_folder="app/templates")

    app.config.from_object(Config)
    db.init_app(app)
    return app


def main():
    delete_database()
    db = SQLAlchemy(model_class=Base)
    app = create_app(db)

    with app.app_context():
        db.create_all()

        session = db.session

        from app.routes.show_routes import register_routes

        register_routes(app, db)

        migrate = Migrate(app, db)

        venue_repository = VenueRepository(session)
        show_repository = ShowRepository(session)
        person_repository = PersonRepository(session)

        venue_repository.add_multiple(venues)
        show_repository.add(nofx_show)
        show_repository.add(nfg_show)
        session.commit()

    return app


if __name__ == "__main__":
    main()
