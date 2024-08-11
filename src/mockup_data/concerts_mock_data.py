from datetime import datetime
from src.entities.Address import Address
from src.entities.Venue import Venue
from src.entities.Concert import Concert
from src.entities.Artist import Artist
from src.entities.Festival import Festival
from src.entities.Person import Person
from src.entities.Photo import Photo
from src.entities.Video import Video
from src.entities.Show import Show


fillmore = Venue(name="The Fillmore", address=None)
red_rocks = Venue(name="Red Rocks")
hollywood_bowl = Venue(name="Hollywood Bowl")
msg = Venue(name="Madison Square Garden")
wrigley = Venue(name="Wrigley Field")
chicago_theatre = Venue(name="Chicago Theatre")
ewerk = Venue(name="E-Wek")

fillmore.address = Address(city="San Francisco", country="USA")
red_rocks.address = Address(city="Morrison", country="USA")
hollywood_bowl.address = Address(city="Los Angeles", country="USA")
msg.address = Address(city="New York", country="USA")
ewerk.address = Address(city="Saarbrücken", country="Germany")
chicago = Address(city="Chicago", country="USA")
wrigley.address = chicago
chicago_theatre.address = chicago

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
    
nofx_show.venue = ewerk
nofx_show.attendees = nofx_show_attendees
