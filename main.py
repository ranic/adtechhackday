import twython
from twython import Twython
from pprint import pprint as pp
import pickle

APP_KEY = 'D1NJ7UyELkVqiWlCIZaa6bwzb'
APP_SECRET = 'zdocY5HBY8Jv6q8daVGYEi7LpkCBeB0SuseW1ijRM9ny0N5w7j'
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
with open('trending_locations.txt', 'r') as f:
    trending_locations = pickle.load(f)

trends_by_location = dict()

with open('trends_by_location.txt', 'w+') as f:
    pickle.dump(trends_by_location, f);

with open('trends_by_location.txt', 'r') as f:
    trends_by_location = pickle.load(f)

pp(trends_by_location)
