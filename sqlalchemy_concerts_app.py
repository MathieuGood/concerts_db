from sqlalchemy import create_engine, Column, String, Integer, Date, Float, ForeignKey, Text, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# Association table for the many-to-many relationship between Concert and Artist
concert_artists = Table(
    'concert_artists', Base.metadata,
    Column('concert_id', ForeignKey('concerts.id'), primary_key=True),
    Column('artist_id', ForeignKey('artists.id'), primary_key=True)
)

# Association table for the many-to-many relationship between Concert and Person
concert_attendees = Table(
    'concert_attendees', Base.metadata,
    Column('concert_id', ForeignKey('concerts.id'), primary_key=True),
    Column('person_id', ForeignKey('people.id'), primary_key=True)
)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    zip = Column(String, nullable=False)
    country = Column(String, nullable=False)

class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String)

class Festival(Base):
    __tablename__ = 'festivals'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)

class Venue(Base):
    __tablename__ = 'venues'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    address = relationship('Address')

class Concert(Base):
    __tablename__ = 'concerts'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    venue_id = Column(Integer, ForeignKey('venues.id'), nullable=False)
    price = Column(Float)
    festival_id = Column(Integer, ForeignKey('festivals.id'))
    comments = Column(Text)

    venue = relationship('Venue')
    festival = relationship('Festival')
    artists = relationship('Artist', secondary=concert_artists, back_populates='concerts')
    attendees = relationship('Person', secondary=concert_attendees, back_populates='concerts')

Artist.concerts = relationship('Concert', secondary=concert_artists, back_populates='artists')
Person.concerts = relationship('Concert', secondary=concert_attendees, back_populates='attendees')

# Setting up the SQLite database
engine = create_engine('sqlite:///concerts.db')
Base.metadata.create_all(engine)

# Creating a new session
Session = sessionmaker(bind=engine)
session = Session()

# Creating instances and adding them to the session
laiterie = Venue(
    name="La Laiterie",
    address=Address(
        street="Rue du Hohwald", city="Strasbourg", zip="67100", country="France"
    ),
)

descendents = Artist(name="Descendents", country="USA")
hogwash = Artist(name="Hogwash", country="France")
franck = Person(firstname="Franck", lastname="Ludwig")

concert = Concert(
    date=datetime(2024, 6, 14),
    venue=laiterie,
    artists=[descendents, hogwash],
    attendees=[franck],
)

session.add(concert)
session.commit()

# Querying the database to verify
for concert in session.query(Concert).all():
    print(f"Concert on {concert.date} at {concert.venue.name}")
    print("Artists:")
    for artist in concert.artists:
        print(f"- {artist.name} ({artist.country})")
    print("Attendees:")
    for attendee in concert.attendees:
        print(f"- {attendee.firstname} {attendee.lastname}")
    print()
