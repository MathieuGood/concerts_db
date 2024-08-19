from entities.Venue import Venue
from entities.Address import Address
from schemas.VenueSchema import VenueResponse, VenueBase, VenueCreate
from sqlalchemy.orm import Session, joinedload
from schemas.AddressSchema import AddressCreate, AddressResponse
from schemas.ShowSchema import ShowCreate, ShowResponse
from schemas.ArtistSchema import ArtistCreate, ArtistResponse
from schemas.ConcertSchema import ConcertCreate, ConcertResponse
from schemas.FestivalSchema import FestivalCreate, FestivalResponse
from schemas.PersonSchema import PersonCreate, PersonResponse
from schemas.PhotoSchema import PhotoCreate, PhotoResponse
from schemas.VenueSchema import VenueCreate, VenueResponse
from schemas.VideoSchema import VideoCreate, VideoResponse
from entities.Address import Address
from entities.Artist import Artist
from entities.Concert import Concert
from entities.Festival import Festival
from entities.Person import Person
from entities.Photo import Photo
from entities.Show import Show
from entities.Video import Video


# Create a new address
def create_address(db: Session, address: AddressCreate):
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


# Retrieve an address by ID
def get_address(db: Session, address_id: int):
    return db.query(Address).filter(Address.id == address_id).first()


# Retrieve all addresses
def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Address).offset(skip).limit(limit).all()


# Create a new venue
def create_venue(db: Session, venue: VenueCreate, address_id: int):
    db_venue = Venue(**venue.dict(), address_id=address_id)
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue


# Retrieve a venue by ID
def get_venue(db: Session, venue_id: int):
    return (
        db.query(Venue)
        .options(joinedload(Venue.address))
        .filter(Venue.id == venue_id)
        .first()
    )


# Retrieve all venues
def get_venues(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Venue)
        .options(joinedload(Venue.address))
        .offset(skip)
        .limit(limit)
        .all()
    )


# Create a new show
def create_show(db: Session, show: ShowCreate, venue_id: int):
    db_show = Show(**show.dict(), venue_id=venue_id)
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show


# Retrieve a show by ID
def get_show(db: Session, show_id: int):
    return (
        db.query(Show)
        .options(joinedload(Show.venue).joinedload(Venue.address))
        .filter(Show.id == show_id)
        .first()
    )


# Retrieve all shows
def get_shows(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Show)
        .options(joinedload(Show.venue).joinedload(Venue.address))
        .offset(skip)
        .limit(limit)
        .all()
    )


# Delete an address
def delete_address(db: Session, address_id: int):
    db_address = get_address(db, address_id)
    if db_address:
        db.delete(db_address)
        db.commit()
    return db_address


# Delete a venue
def delete_venue(db: Session, venue_id: int):
    db_venue = get_venue(db, venue_id)
    if db_venue:
        db.delete(db_venue)
        db.commit()
    return db_venue


# Delete a show
def delete_show(db: Session, show_id: int):
    db_show = get_show(db, show_id)
    if db_show:
        db.delete(db_show)
        db.commit()
    return db_show
