from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Key : {[(title, date, text), ... , (title, date, text)]

#class ArticlesManager(models.Model):
#    article = models.TextField()

class Article(models.Model):
    title = models.TextField()
    pub_date = models.DateField('date_published')
    nltk_score = models.IntegerField(default=0)
    source = models.TextField()

    #objects = ArticlesManager()


    def __str__(self):
        return self.title
'''
class ProPublica(models.Model):

    article_title = models.ForeignKey(Forum, on_delete=models.CASCADE)
    author = models.TextField()
    pub_date = models.DateTimeField('date_published')
    nltk_score = models.IntegerField(default=0)

    def __str__(self):
        return self.title
'''

    