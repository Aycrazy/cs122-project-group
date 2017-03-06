from django.contrib import admin
from newsapp.models import ArticlesManager, Article
import csv
# Register your models here.

admin.site.register(ArticlesManager)
admin.site.register(Article)


#Find the file -- python any csv in the file path 
#Figure out exactly where this is to run

