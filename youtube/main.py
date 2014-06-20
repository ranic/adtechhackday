import urllib2
import json # derulo
import pprint


def get_id(url):
    """
    Retrieve the id of a video given its URL
    url: string
    """
    return url.split('v=')[1]

def get_json(video_id):
    """
    Retrieve the JSON object associated with a video
    video_id: string
    """
    URL = 'http://gdata.youtube.com/feeds/api/videos/' + video_id + '?v=2&alt=jsonc'
    res = urllib2.urlopen(URL)

    return json.load(res)

def get_category(video_id):
    """
    Return the category of a video given its ID
    video_id: string
    """
    json_object = get_json(video_id)

    return json_object['data']['category']


if __name__ == '__main__':
    print get_id('https://www.youtube.com/watch?v=IAQ112vC3Qg')
    print get_category('6BTjG-dhf5s')



