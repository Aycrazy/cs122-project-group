from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Key : {[(title, date, text), ... , (title, date, text)]

#class ArticlesManager(models.Model):
#    article = models.TextField()

class Date(models.Model):
    date = models.DateField(primary_key=True,default=0)
    id = models.IntegerField(default=0)

class Article(models.Model):
    title = models.TextField(primary_key=True)
    date = models.ForeignKey(Date)
    nltk_score = models.FloatField(default=0)
    nltk_score_title= models.FloatField(default=0)
    source = models.TextField()

    def __str__(self):
        return str([self.title,self.date,self.nltk_score,self.source])

class Ticker(models.Model):
    date = models.ForeignKey(Date)
    close = models.FloatField(default=0)
    ticker = models.TextField()
    id = models.IntegerField(primary_key=True)

class Currency(models.Model):
    date = models.ForeignKey(Date)
    exchange_rate = models.FloatField(default=0)
    peso = models.FloatField()
    id = models.IntegerField(primary_key=True)

    