from datetime import datetime
from models.address import Address
from models.venue import Venue
from models.concert import Concert
from models.artist import Artist
from models.festival import Festival
from models.attendee import Attendee
from models.photo import Photo
from models.video import Video
from models.show import Show


fillmore = Venue(name="The Fillmore", address=None)
fillmore.address = Address(city="San Francisco", country="USA")
red_rocks = Venue(name="Red Rocks")
red_rocks.address = Address(city="Morrison", country="USA")
hollywood_bowl = Venue(name="Hollywood Bowl")
hollywood_bowl.address = Address(city="Los Santos", country="USA")
msg = Venue(name="Madison Square Garden")
msg.address = Address(city="New York", country="USA")
wrigley = Venue(name="Wrigley Field")
chicago_theatre = Venue(name="Chicago Theatre")
chicago = Address(city="Chicago", country="USA")
wrigley.address = chicago
chicago_theatre.address = chicago
ewerk = Venue(name="E-Werk")
ewerk.address = Address(city="Saarbrücken", country="Germany")
hob_boston = Venue(name="House of Blues Boston")
hob_boston.address = Address(city="Boston", country="USA")
laiterie = Venue(name="La Laiterie")
laiterie.address = Address(city="Strasbourg", country="France")
la_cigale = Venue(name="La Cigale")
paris = Address(city="Paris", country="France")
la_cigale.address = paris
bataclan = Venue(name="Bataclan")
bataclan.address = paris
zenith = Venue(name="Zenith de Nantes")
zenith.address = Address(city="Nantes", country="France")
achenheim = Venue(name="Le Cheval Blanc")
achenheim.address = Address(city="Achenheim", country="France")
grillen = Venue(name="Le Grillen")
grillen.address = Address(city="Colmar", country="France")
batofar = Venue(name="Batofar")
batofar.address = paris

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
    achenheim,
    grillen,
    batofar,
]

festivals = [
    Festival(
        name="Punk Rock Bowling",
    ),
    Festival(
        name="Hellfest",
    ),
    Festival(
        name="Download",
    ),
    Festival(
        name="Rock en Seine",
    ),
]

coralsprings_address = Address(city="Coral Springs", country="USA")
losangeles_address = Address(city="Los Angeles", country="USA")
london_address = Address(city="London", country="England")

nofx_show_artists = [
    Artist(name="The Last Gang", address=losangeles_address),
    Artist(name="The Meffs", address=london_address),
    Artist(name="NOFX", address=losangeles_address),
]

nofx_show_attendees = [
    Attendee(firstname="Franck", lastname="Ludwig"),
    Attendee(firstname="Agnès", lastname="Maillard"),
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

nfg_show = Show(event_date=datetime(year=2009, month=4, day=30))
nfg_show.venue = hob_boston
nfg_concert = Concert()

nfg_concert.artist = Artist(name="New Found Glory", address=coralsprings_address)
nfg_concert.comments = "They played all their hits!"
nfg_show.concerts.append(nfg_concert)
