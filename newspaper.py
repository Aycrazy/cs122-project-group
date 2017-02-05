# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import urllib3
import csv
import html5lib
from io import StringIO
import newspaper
from newspaper import Article
import re

main_url_usa = 'http://www.usatoday.com/'
main_url_la = 'http://www.latimes.com/'

def newspaper_use(my_url):
    article = Article(my_url, language='es')
    article.download()
    article.html
    article.parse()
    return article.parse()

def get_authors(parse):
    return parse.authors

def get_text(parse):
    return parse.text

def get_articles(main_url):
    jornada = newspaper.build(main_url)
    articles = []
    for article in jornada.articles:
        articles.append(article.url)
    return articles

