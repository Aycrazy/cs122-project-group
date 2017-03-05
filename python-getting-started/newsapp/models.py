from django.db import models

# Create your models here.

#Key : {[(title, date, text), ... , (title, date, text)]

class ArticlesManager(models.Model):
    def create_article(self,title, pub_date, nltk_score, source):
        article = self.create(title = title, pub_date = pub_date,\
            nltk_score = nltk_score, source = source)
        return article

class Article(models.Model):
    article_title = models.ForeignKey(ArticlesManager, on_delete=models.CASCADE)
    author = models.TextField()
    pub_date = models.DateTimeField('date_published')
    nltk_score = models.IntegerField(default=0)
    source = models.TextField()

    objects = ArticlesManager()


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

    