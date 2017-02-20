
import urllib3
import bs4
import urllib.parse
import requests
import re
from io import StringIO
import newspaper
from newspaper import Article
import random
from random import randint
from time import sleep
import pandas as pd
from newspaper.configuration import Configuration


main_url = "http://www.jornada.unam.mx/ultimas"


user_agents = ["Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0",
             "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0",
             "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
             "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0",
             "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0",
             "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0",
             "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0",
             "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0",
             "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0"]

def get_sections(main_url):

#jornada tag_type = 'li'
#jornada class_type = 'fixed-menu-p'
#latimes tag_type = 'li'
#latimes class_type = 'trb_nh_ln_li'

def get_sections(main_url, tag_type, class_type):

    '''
    Find all the sections in the newspaper
    Inputs: main url 
    Returns: A list with the links for all the sections
    '''
    pm = urllib3.PoolManager()
    html = pm.urlopen(url= main_url, method="GET").data
    soup = bs4.BeautifulSoup(html,'lxml')

    tag_list = soup.find_all(tag_type, class_= class_type)

    rel_links_menu = []
    for t in tag_list: 
        pattern = r'(?<=/)[a-z]+'
        rel = re.findall(pattern, t.a['href'])
        if main_url == "www.latimes.com":
            if len(rel)>0 and (rel[0], main_url + '/' + rel[0]) not in rel_links_menu:
                rel_links_menu.append((rel[1],main_url + '/'+rel[1]))
        elif len(rel)>1 and (rel[1], main_url + '/' + rel[1]) not in rel_links_menu:
            rel_links_menu.append((rel[1],main_url + '/'+rel[1]))

    return rel_links_menu

#jornado tag_type = 'h3'
#latimes tag_type = 'h4'
#latimes class_type = 'trb_outfit_relatedListTitle'

def get_articles(sections_list, tag_type, class_type=None):
    '''
    Retrieve articles from every section in the 
    list of sections
    Inputs: A list of sections
    Returns: A dictionary where each key corresponds
    to a section and contains the list of links for every
    article in that section
    '''
    articles = {}
    pm = urllib3.PoolManager()
    for key, s in sections_list:
      
        html = pm.urlopen(url= s, method="GET").data

        soup = bs4.BeautifulSoup(html, 'lxml')
        if class_type:
            tag_list = soup.find_all(tag_type, class_ = class_type)
        else:
            tag_list = soup.find_all(tag_type)
        
        for tag in tag_list:
            article = tag.a['href']
           
            if key not in articles:
                articles[key]= []
            articles[key].append(article)

    for  key, item in articles.items():
        articles[key] = list(set(articles[key]))

    return articles

def get_info(dictionary):
    '''
    '''
    rv = {}
    for key, item in dictionary.items():
        count = 0
        for i in item:
            sleep(randint(5,15))
            #config = Configuration()
            #config.browser_user_agent = random.choice(user_agents)
            article = Article(i, language = 'es')
            
            #article.download()
            article.build()
            count = count + 1
            title = article.title
            print(title, key, count)
            date = article.publish_date
            text = article.text
            if key not in rv:
                rv[key] = []
            rv[key].append((title, date, text))

    return rv
