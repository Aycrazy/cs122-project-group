from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

# Create your models here.

#Key : {[(title, date, text), ... , (title, date, text)]

class Forum(models.Model):
    article_title = models.TextField()
    homepage = models.URLField()

class Jornada(models.Model):

    section = models.TextField()
    article_title = models.ForeignKey(Forum, on_delete=models.CASCADE)
    author = models.TextField()
    pub_date = models.DateTimeField('date_published')
    nltk_score = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class ProPublica(models.Model):

    article_title = models.ForeignKey(Forum, on_delete=models.CASCADE)
    author = models.TextField()
    pub_date = models.DateTimeField('date_published')
    nltk_score = models.IntegerField(default=0)

    def __str__(self):
        return self.title


    