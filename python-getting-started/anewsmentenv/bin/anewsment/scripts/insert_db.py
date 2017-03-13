#!/bin/bash
from newsapp.models import Article, Date, Currency, Ticker
#from scripts import
from django.utils import timezone
from scripts.translate import translate_keywords
import re
import glob, os
import csv
import manage
import datetime

def get_date_ints(article_date):
    if '/' in article_date:
        pattern = r'(?<=0)\d|\d{4}|[^/0]\d*'
    else:
        pattern = r'(?<=0)\d|\d{4}|[^-0]\d*'

    date_ints = re.findall(pattern, article_date)
    #print(date_ints)
    y,m,d = date_ints
    return datetime.date(int(y),int(m),int(d))
  
def run():

    for file in glob.glob("*.csv"):
        with open(file, 'r') as csvfile:    
            if 'jornada' in file or 'propublica' in file or 'chicago' in file:
                reader = csv.reader(csvfile)
                next(reader,None)
                for row in reader:
                    if 'propublica' in file or 'chicago' in file:
                        dj = Date(pk=get_date_ints(row[1]))
                    else:
                        dj = Date(pk=row[1])
                    print('date_correct ran')
                   
                    print(row[2],row[3],row[4])
                    article = dj.article_set.create(title=row[0],\
                        nltk_score=row[2], nltk_score_title = row[4], source = row[3])
                    #article = Article.objects.create(title=translate_keywords(row[0]),\
                    #    date = dj, nltk_score=row[2], nltk_score_title = row[4], source = row[3])
                    
                    print('should be created')
                    #break
            elif 'stock' in file:
                reader = csv.reader(csvfile)
                next(reader, None)
                for row in reader:
                    ticker = Ticker(date=row[0],close=row[1],ticker=row[2])
                ticker.save()
            elif 'currency' in file:
                reader = csv.reader(csvfile)
                next(reader,None)
                for row in reader:
                    currency = Currency(date=row[0],exchange_rate=row[1],peso=row[2])
                currency.save()
        print('test')
        os.remove(file)
