import urllib2
import json # derulo
import pprint

def retrieve_JSON(video_id):
    """
    Retrieve the JSON object associated with a video
    video_id: string
    """
    URL = 'http://gdata.youtube.com/feeds/api/videos/' + videoID + '?v=2&alt=jsonc'
    res = urllib2.urlopen(URL)

    return json.load(res)

def get_category(video_id):
    """
    Return the category of a video given its ID
    video_id: string
    """
    JSON = retrieve_JSON(video_id)

    return JSON['data']['category']


if __name__ == '__main__':
    print get_category('6BTjG-dhf5s')



