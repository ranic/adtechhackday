from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_init
import urllib2
import json

LONG = 500
NUM_RELATED_VIDS = 5

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
    self.related_videos = [text['data']['items'][i]['id'] for i in xrange(NUM_RELATED_VIDS)]
    self.save()

post_init.connect(extraInitForAd, Ad)


class AdUser(models.Model):
    user = models.OneToOneField(User)
    score = models.IntegerField()
    favoriteCategory = models.CharField(max_length=LONG)
    favoriteCategoryCounts = {}
    recommended = models.ManyToManyField(Ad, related_name='recommended_by') 
    blacklisted = models.ManyToManyField(Ad, related_name='blacklisted_by') # user has disliked these, so he cannot be referred to them 

    def incrementScore(self, amount=1):
        self.score += amount
        self.save()

    def recommend(self, ads):
        for ad_id in ads:
            a, _ = Ad.objects.get_or_create(url_id=ad_id)
            self.recommended.add(a)
        self.save()

    def blacklist(self, ad_id):
        # Add to blacklist and remove from recommended, if it exists
        self.blacklisted.add(Ad.objects.get(url_id=ad_id))
        try:
            a = self.recommended.get(url_id=ad_id)
            recommended.remove(a)
        except Exception as e:
            pass   
         

        self.save()

    def updateFavorite(self, category):
        if not category in self.favoriteCategoryCounts:
            self.favoriteCategoryCounts[category] = 0
        self.favoriteCategoryCounts[category] += 1
        if not self.favoriteCategory:
            self.favoriteCategory = category   
        if self.favoriteCategoryCounts[category] > self.favoriteCategoryCounts[self.favoriteCategory]:
            self.favoriteCategory = category

        self.save()

        
class SharedAd(models.Model):
    ad = models.ForeignKey(Ad)
    sent_by = models.ForeignKey(AdUser, related_name="sent_by")
    sent_to = models.ForeignKey(AdUser, related_name="sent_to")
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)
    url = models.CharField(max_length=LONG)

    def like(self):
        self.is_liked = True
        self.sent_to.recommend(self.ad.related_videos) # recommend related videos
        self.sent_to.updateFavorite(self.ad.category)
        self.sent_by.incrementScore()
        self.save()

    def dislike(self):
        self.is_liked = False
        self.is_disliked = True
        self.sent_to.blacklist(self.ad.url_id)
        self.sent_by.incrementScore(-1)
        self.save()

