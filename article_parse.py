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

def get_sections(main_url):
    paper = newspaper.build(main_url)
    articles = []
    for article in paper.categories:
        articles.append(article.url)
    return articles
'''
def get_sections_la('main_url'): # we could just add 3 parameters to Juan's version (tag_type, class_type, pattern)
        '''
    Find all the sections in the newspaper
    Inputs: main url 
    Returns: A list with the links for all the sections
    '''
    pm = urllib3.PoolManager()
    html = pm.urlopen(url= main_url, method="GET").data
    soup = bs4.BeautifulSoup(html,'lxml')

    tag_list = soup.find_all('li', class_="trb_nh_ln_li")

    rel_links_menu = []
    for t in tag_list: 
        pattern = r'(?<=/)[a-z]+'
        rel = re.findall(pattern, t.a['href'])
        if len(rel)>1 and (rel[0], main_url + '/' + rel[1]) not in rel_links_menu: #make sure rel[0] is right
            rel_links_menu.append((rel[1],main_url + '/'+rel[1]))

    return rel_links_menu


def get_articles(sections_list):# add 2 parameters to Juan's function (tag_type, class_type)

    <--Retrieve articles from every section in the 
    list of sections
    Inputs: A list of sections
    Returns: A dictionary where each key corresponds
    to a section and contains the list of links for every
    article in that section-->
    
    articles = {}
    pm = urllib3.PoolManager()
    for key, s in sections_list:
      
        html = pm.urlopen(url= s, method="GET").data

        soup = bs4.BeautifulSoup(html, 'lxml')
        tag_list = soup.find_all('h3', class__='trb_outfit_relatedListTitle')
        
        for tag in tag_list:
            article = tag.a['href']
           
            if key not in articles:
                articles[key]= []
            articles[key].append(article)

    for  key, item in articles.items():
        articles[key] = list(set(articles[key]))

    return articles
'''


