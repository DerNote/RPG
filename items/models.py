from django.db import models
from utils import db

# Create your models here.

Items_collection = db['Items']
Feats_collection = db['feats']
Flaws_collection = db['flaws']
Player_collection = db['Players']
    
class Player(models.Model):
    name = models.CharField(max_length=100)
    hp_current = models.IntegerField()
    hp_max = models.IntegerField()

class Message(models.Model):
    room_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.content}"