# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import urllib3
import csv
import html5lib
from io import StringIO#
import newspaper
#from newspaper import Article
import re

main_url_usa = 'http://www.usatoday.com/'
main_url_la = 'http://www.latimes.com/'
main_url_pro= 'https://www.propublica.org'

def newspaper_usEN(my_url):
    article = newspaper.build(my_url)
    article.download()
    article.html
    article.parse()
    return article.parse()

def newspaper_usES(my_url):
    article = Article(my_url, language = 'es')
    article.download()
    article.html
    article.parse()
    return article.parse()

def get_title(parse):
    return parse.title
    
def get_authors(parse):
    return parse.authors
    
def get_keywords(parse):
    parse.nlp()
    return parse.kewords

def get_text(parse):
    return parse.text
    
def get_pdate(parse):
    return parse.publish_date

def get_articles(main_url):
    jornada = newspaper.build(main_url)
    articles = []
    for article in jornada.articles:
        articles.append(article.url)
    return articles

