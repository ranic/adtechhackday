import urllib2
import json

import sys

if len(sys.argv) == 2:
	id = sys.argv[1]
	target_url = 'https://gdata.youtube.com/feeds/api/videos/' + id + '?v=2&alt=jsonc'
else:
	target_url = 'https://gdata.youtube.com/feeds/api/videos/0B04--XmZiE?v=2&alt=jsonc'

text = urllib2.urlopen(target_url)

text = json.load(text)
uploader = text['data']['uploader']
category = text['data']['category']



similars_url = "https://gdata.youtube.com/feeds/api/videos?author=" + uploader + "&v=2&orderby=updated&alt=jsonc"

text = urllib2.urlopen(similars_url)
text = json.load(text)

url_list = []

for i in range(10):
	url_list.append('https://www.youtube.com/watch?v='+text['data']['items'][i]['id'])

print 'Uploader:', uploader
print 'Category: ', category
print 'Recommended: ',url_list
