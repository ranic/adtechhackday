from django.db import models
from django.contrib.auth.models import User

class AdUser(models.Model):
    user = models.OneToOneField(User)
    score = models.IntegerField()
    favorite_category = models.CharField()
    recommended = []

    def incrementScore(self, amount=1):
        self.score += amount
        self.save()


class Ad(models.Model):
    category = models.CharField()
    uploader = models.CharField()
    url = models.CharField()
    related_videos = []

    def get_id(self):
        return self.url.split("v=")[1] # TODO


class SharedAd(models.Model):
    ad = models.ForeignKey(Ad)
    sent_by = models.ForeignKey(AdUser)
    sent_to = models.ForeignKey(AdUser)
    is_liked = models.BooleanField(default=False)
    url = models.CharField()

    def like(self):
        # Grow his list of recommended videos in that category
        self.is_liked = True
        self.sent_to.recommended += related
        self.sent_by.incrementScore()

