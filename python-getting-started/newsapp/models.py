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
    source = models.TextField()
    def __str__(self):
        return self.title

class Ticker(models.Model):
    date = models.ManyToManyField(Article)
    close = models.FloatField(default=0)
    ticker = models.TextField()

class Currency(models.Model):
    date = models.ManyToManyField(Article)
    currency = models.FloatField(default=0)
    country = models.TextField()


    