from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AdUser(models.Model):
    user = models.OneToOneField(User)
    score = models.IntegerField()
    
    def incrementScore(self, amount=1):
        self.score += amount
        self.save()
