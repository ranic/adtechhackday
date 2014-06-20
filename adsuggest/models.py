from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_init
import urllib2
import json

LONG = 500

class AdUser(models.Model):
    user = models.OneToOneField(User)
    score = models.IntegerField()
    favorite_category = models.CharField(max_length=LONG)
    recommended = []

    def incrementScore(self, amount=1):
        self.score += amount
        self.save()

    def recommend(self, ads):
        self.recommended += ads
        self.save()

class Ad(models.Model):
    category = models.CharField(max_length=LONG)
    uploader = models.CharField(max_length=LONG)
    url_id = models.CharField(max_length=LONG, primary_key=True)
    related_videos = []

    def get_url(self):
        return "http://www.youtube.com/watch?v=" + self.url_id
    
    def embedUrl(self):
        return "http://www.youtube.com/embed/" + self.url_id

def extraInitForAd(**kwargs):
    self = kwargs.get('instance')
    url_id = self.url_id
    target_url = 'https://gdata.youtube.com/feeds/api/videos/' + url_id + '?v=2&alt=jsonc'
    text = json.load(urllib2.urlopen(target_url))
    self.uploader = text['data']['uploader']
    self.category = text['data']['category']

    similar_videos_url = "https://gdata.youtube.com/feeds/api/videos?author=" + self.uploader + "&v=2&orderby=updated&alt=jsonc"
    text = json.load(urllib2.urlopen(similar_videos_url))
    self.related_videos = ['https://www.youtube.com/watch?v='+text['data']['items'][i]['id'] for i in xrange(10)]
    self.save()

post_init.connect(extraInitForAd, Ad)

class SharedAd(models.Model):
    ad = models.ForeignKey(Ad)
    sent_by = models.ForeignKey(AdUser, related_name="sent_by")
    sent_to = models.ForeignKey(AdUser, related_name="sent_to")
    is_liked = models.BooleanField(default=False)
    url = models.CharField(max_length=LONG)

    def like(self):
        # Grow his list of recommended videos in that category
        self.is_liked = True
        self.sent_to.recommend(self.ad.related_videos)
        self.sent_by.incrementScore()
        self.save()

