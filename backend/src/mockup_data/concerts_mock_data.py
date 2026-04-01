from datetime import datetime
from models.country import Country
from models.city import City
from models.venue import Venue
from models.concert import Concert
from models.artist import Artist
from models.festival import Festival
from models.attendee import Attendee
from models.photo import Photo
from models.video import Video
from models.event import Event


usa = Country(name="USA")
germany = Country(name="Germany")
france = Country(name="France")
england = Country(name="England")

san_francisco = City(name="San Francisco", country=usa)
morrison = City(name="Morrison", country=usa)
los_santos = City(name="Los Santos", country=usa)
new_york = City(name="New York", country=usa)
chicago = City(name="Chicago", country=usa)
saarbruecken = City(name="Saarbrücken", country=germany)
boston = City(name="Boston", country=usa)
strasbourg = City(name="Strasbourg", country=france)
paris = City(name="Paris", country=france)
nantes = City(name="Nantes", country=france)
achenheim = City(name="Achenheim", country=france)
colmar = City(name="Colmar", country=france)
coral_springs = City(name="Coral Springs", country=usa)
los_angeles = City(name="Los Angeles", country=usa)
london = City(name="London", country=england)
truchtersheim = City(name="Truchtersheim", country=france)
wittenheim = City(name="Wittenheim", country=france)

fillmore = Venue(name="The Fillmore", city=san_francisco)
red_rocks = Venue(name="Red Rocks", city=morrison)
hollywood_bowl = Venue(name="Hollywood Bowl", city=los_santos)
msg = Venue(name="Madison Square Garden", city=new_york)
wrigley = Venue(name="Wrigley Field", city=chicago)
chicago_theatre = Venue(name="Chicago Theatre", city=chicago)
ewerk = Venue(name="E-Werk", city=saarbruecken)
hob_boston = Venue(name="House of Blues Boston", city=boston)
laiterie = Venue(name="La Laiterie", city=strasbourg)
la_cigale = Venue(name="La Cigale", city=paris)
bataclan = Venue(name="Bataclan", city=paris)
zenith = Venue(name="Zenith de Nantes", city=nantes)
achenheim_venue = Venue(name="Le Cheval Blanc", city=achenheim)
grillen = Venue(name="Le Grillen", city=colmar)
batofar = Venue(name="Batofar", city=paris)

venues = [
    fillmore,
    red_rocks,
    hollywood_bowl,
    msg,
    wrigley,
    chicago_theatre,
    ewerk,
    hob_boston,
    laiterie,
    la_cigale,
    bataclan,
    zenith,
    achenheim_venue,
    grillen,
    batofar,
]

other_festivals = [
    Festival(name="Punk Rock Bowling"),
    Festival(name="Hellfest"),
    Festival(name="Download"),
    Festival(name="Rock en Seine"),
    Festival(name="Punk In Drublic"),
]

nofx_artists = [
    Artist(name="The Last Gang", country=los_angeles.country),
    Artist(name="The Meffs", country=england),
    Artist(name="NOFX", country=usa),
]

nofx_attendees = [
    Attendee(firstname="Eric", lastname="Idle"),
    Attendee(firstname="Michael", lastname="Palin"),
]

nofx_event = Event(
    event_date=datetime(year=2024, month=6, day=1),
    comments="The only good show was NOFX.",
)


nofx_concerts = [
    Concert(
        artist=nofx_artists[0],
        comments="Totally overrated band",
    ),
    Concert(artist=nofx_artists[1]),
    Concert(
        artist=nofx_artists[2],
        comments="They played the Decline, it was huge.",
        setlist="60%, Play Video, The Man I Killed, Benny Got Blowed Up",
    ),
]

for concert in nofx_concerts:
    concert.event = nofx_event


nofx_event.concerts[2].photos = [
    Photo(path="Photo of Fat Mike"),
    Photo(path="Photo of Eric Melvin"),
]
nofx_event.concerts[2].videos = [
    Video(path="Video of The Decline"),
    Video(path="Video of Linoleum"),
]
nofx_event.name = "NOFX Final Tour"
nofx_event.venue = ewerk
nofx_event.attendees = nofx_attendees
nofx_event.festival = other_festivals[4]

nfg_event = Event(event_date=datetime(year=2009, month=4, day=30))
nfg_event.attendees = [
    Attendee(firstname="Laurent", lastname="Broomhead"),
]
nfg_event.comments = "One of my best show nights ever"
nfg_event.venue = hob_boston
nfg_concert = Concert()
nfg_concert.photos = [
    Photo(path="Photo of Jordan Pundik"),
    Photo(path="Photo of Chad Gilbert"),
]
nfg_concert.videos = [
    Video(path="Video of My Friends Over You"),
    Video(path="Video of Hit or Miss"),
]

nfg_concert.artist = Artist(name="New Found Glory", country=usa)
nfg_concert.comments = "They played all their hits! I got Cyrus's drumstick."
nfg_concert.event = nfg_event


other_artists = [
    Artist(name="The Offspring", country=usa),
    Artist(name="Rancid", country=usa),
    Artist(name="Pennywise", country=usa),
    Artist(name="Bad Religion", country=usa),
    Artist(name="Green Day", country=usa),
]

other_attendees = [
    Attendee(firstname="Graham", lastname="Chapman"),
    Attendee(firstname="John", lastname="Cleese"),
]
