#!/bin/bash
from newsapp.models import Article #, ArticlesManager
#from scripts import
from django.utils import timezone
import re
import glob, os
import csv
import manage

def get_date_ints(article_date):
    date_ints= None
    pattern = r'(?<=0)\d|\d{4}|[^/0]\d*'
    #for article_date in article_dates:
    date_ints = re.findall(pattern, article_date)
    print(date_ints)
    y,m,d = date_ints[0]
    return datetime.date(int(y),int(m),int(d))


def run():
    #os.chdir("scripts")
    print(os.getcwd())
    for file in glob.glob("*.csv"):
        print(file)
        with open(file, 'r') as csvfile:
            print('hello')
            reader = csv.reader(csvfile)
            next(reader,None)
            print('hellos')
            for row in reader:
                date_correct = get_date_ints(row[1])
                article = Article.objects.create(title=row[0],pub_date=date_correct,\
                    nltk_score=row[2],source = row[3])
                article.save()
