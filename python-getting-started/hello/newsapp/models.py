from django.db import models

# Create your models here.

#Key : {[(title, date, text), ... , (title, date, text)]

class Forum(models.Model):
    section = models.TextField()
    homepage = models.URLField()

class Jornada(models.Model):

    section = models.ForeignKey(Forum, on_delete=models.CASCADE)
    title = models.TextField(primary_key=True)
    author = models.TextField()
    pub_date = models.DateTimeField('date_published')
    nltk_score = models.IntegerField(default=0)

    def __str__(self):
        return self.title



    