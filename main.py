import twython
from twython import Twython
from pprint import pprint as pp

APP_KEY = 'D1NJ7UyELkVqiWlCIZaa6bwzb'
APP_SECRET = 'zdocY5HBY8Jv6q8daVGYEi7LpkCBeB0SuseW1ijRM9ny0N5w7j'
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

obama = twitter.search(q='@BarackObama')
print "Obama results:"
pp(obama)

worldCup = twitter.search(q='#WorldCup')
print "WorldCup results: "
pp(worldCup)
