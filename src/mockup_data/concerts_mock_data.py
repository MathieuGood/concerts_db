from datetime import datetime
from entities.Address import Address
from entities.Venue import Venue
from entities.Concert import Concert
from entities.Artist import Artist
from entities.Festival import Festival
from entities.Person import Person
from entities.Photo import Photo
from entities.Video import Video
from entities.Show import Show


fillmore = Venue(name="The Fillmore", address=None)
fillmore.address = Address(city="San Francisco", country="USA")
red_rocks = Venue(name="Red Rocks")
red_rocks.address = Address(city="Morrison", country="USA")
hollywood_bowl = Venue(name="Hollywood Bowl")
hollywood_bowl.address = Address(city="Los Angeles", country="USA")
msg = Venue(name="Madison Square Garden")
msg.address = Address(city="New York", country="USA")
wrigley = Venue(name="Wrigley Field")
chicago_theatre = Venue(name="Chicago Theatre")
chicago = Address(city="Chicago", country="USA")
wrigley.address = chicago
chicago_theatre.address = chicago
ewerk = Venue(name="E-Wek")
ewerk.address = Address(city="Saarbrücken", country="Germany")
venues = [fillmore, red_rocks, hollywood_bowl, msg, wrigley, chicago_theatre, ewerk]

nofx_show_artists = [
    Artist(name="Circle Jerks", country="USA"),
    Artist(name="Itchy", country="USA"),
    Artist(name="The Last Gang", country="USA"),
    Artist(name="The Meffs", country="England"),
]

nofx_show_attendees = [
    Person(firstname="Franck", lastname="Ludwig"),
    Person(firstname="Agnès", lastname="Maillard"),
]

nofx_show = Show(
    event_date=datetime(year=2024, month=6, day=1),
    comments="NOFX played The Decline, it was exceptional",
)


for artist in nofx_show_artists:
    concert = Concert()
    concert.artist = artist
    concert.show = nofx_show

nofx_show.name = "NOFX Final Tour"
nofx_show.venue = ewerk
nofx_show.attendees = nofx_show_attendees
