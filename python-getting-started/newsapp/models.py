from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Key : {[(title, date, text), ... , (title, date, text)]

#class ArticlesManager(models.Model):
#    article = models.TextField()

class Article(models.Model):
    title = models.TextField()
    pub_date = models.DateField('date_published')
    nltk_score = models.FloatField(default=0)
    nltk_score_title= models.FloatField(default=0)
    source = models.TextField()

    def __str__(self):
        return str([self.title,self.pub_date,self.nltk_score,self.source])

class Ticker(models.Model):
    date = models.DateField('date_published')
    close = models.FloatField(default=0)
    ticker = models.TextField()

class Currency(models.Model):
    date = models.DateField('date_published')
    currency = models.FloatField(default=0)
    peso = models.TextField()

    