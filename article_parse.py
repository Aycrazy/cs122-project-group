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
from newspaper import Article
import re

main_url_usa = 'http://www.usatoday.com/'
main_url_la = 'http://www.latimes.com/'
main_url_pro= 'https://www.propublica.org/'


def newspaper_usEN(my_url):
    article = Article(my_url)
    article.download()
    article.html
    article.parse()

def newspaper_usES(my_url):
    article = Article(my_url, language = 'es')
    article.download()
    article.html
    article.parse()

def get_title(article):
    return article.title
    
def get_authors(article):
    return article.authors
    
    parse.nlp()
    return article.kewords

def get_text(article):
    return article.text
    
def get_pdate(article):
    return articlepublish_date

def get_articles(main_url):
    paper = newspaper.build(main_url)
    articles = []
    for article in paper.articles:
        articles.append(article.url)
    return articles

