from django.contrib import admin
from newsapp.models import Article, Ticker, Currency, Date
import csv
# Register your models here.

#admin.site.register(ArticlesManager)
admin.site.register(Article)
admin.site.register(Ticker)
admin.site.register(Currency)
admin.site.register(Date)

#Find the file -- python any csv in the file path 
#Figure out exactly where this is to run

