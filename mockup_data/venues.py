from src.entities.Address import Address
from src.entities.Venue import Venue

fillmore = Venue(name="The Fillmore")
red_rocks = Venue(name="Red Rocks")
hollywood_bowl = Venue(name="Hollywood Bowl")
msg = Venue(name="Madison Square Garden")
wrigley = Venue(name="Wrigley Field")

fillmore.address = Address(city="San Francisco", country="USA")
red_rocks.address = Address(city="Morrison", country="USA")
hollywood_bowl.address = Address(city="Los Angeles", country="USA")
msg.address = Address(city="New York", country="USA")
wrigley.address = Address(city="Chicago", country="USA")

venues = [fillmore, red_rocks, hollywood_bowl, msg, wrigley]
