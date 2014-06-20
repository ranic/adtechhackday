import urllib2
import json # derulo
import pprint

def retrieve_JSON(videoID):
    URL = 'http://gdata.youtube.com/feeds/api/videos/' + videoID + '?v=2&alt=jsonc'
    res = urllib2.urlopen(URL)

    return json.load(res)

def get_category(videoID):
    JSON = retrieve_JSON(videoID)

    return JSON['data']['category']


if __name__ == '__main__':
    print get_category('6BTjG-dhf5s')



