import urllib2
import json
import pprint

def retrieveJSON(videoID):
    URL = 'http://gdata.youtube.com/feeds/api/videos/' + videoID + '?v=2&alt=jsonc'
    res = urllib2.urlopen(URL)

    yo = json.load(res)

    pprint.pprint(yo)

retrieveJSON('WLYnXyRFxB8')



