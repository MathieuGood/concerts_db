from entities.Address import Address
from entities.Venue import Venue

fillmore = Venue(name="The Fillmore")
red_rocks = Venue(name="Red Rocks")
hollywood_bowl = Venue(name="Hollywood Bowl")
msg = Venue(name="Madison Square Garden")
wrigley = Venue(name="Wrigley Field")
chicago_theatre = Venue(name="Chicago Theatre")

fillmore.address = Address(city="San Francisco", country="USA")
red_rocks.address = Address(city="Morrison", country="USA")
hollywood_bowl.address = Address(city="Los Angeles", country="USA")
msg.address = Address(city="New York", country="USA")
wrigley.address = Address(city="Chicago", country="USA")
chicago_theatre.address = Address(city="Chicago", country="USA")

venues = [fillmore, red_rocks, hollywood_bowl, msg, wrigley, chicago_theatre]
