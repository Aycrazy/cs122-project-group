
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


#main_url = "http://www.jornada.unam.mx/ultimas"
years07_09 = ['2007', '2008', '2009']
years10_16 = ['2010', '2011', '2012', '2013', '2014', '2015', '2016']

def get_user_agent():


    '''
    '''
    user_agents = []

    usertext = pd.read_table('useragents.txt',sep='*', header=None)

    stacked = usertext.stack()

    pd.set_option('display.width', 1000)

    return stacked.sample(1).reset_index()[0][0].strip(" ")




#jornada 10-16 tag_type = 'div'
#jornada 10-16 class_type = 'main-sections gui'
#jornada tag_type = 'li'
#jornada class_type = 'fixed-menu-p'
#latimes tag_type = 'li'
#latimes class_type = 'trb_nh_ln_li'


def get_sections(main_url, tag_type, class_type):

    '''
    Find all the sections in the newspaper
    Inputs: main url 
            jornada 07-09 tag_type = 'a'
            jornada 07-09 class_type = 'visualIconPadding'
            jornada 10-16 tag_type = 'div'
            jornada 10-16 class_type = 'main-sections gui'
            jornada tag_type = 'li'
            jornada class_type = 'fixed-menu-p'
            latimes tag_type = 'li'
            latimes class_type = 'trb_nh_ln_li'

    Returns: A list with the links for all the sections
    '''
    pm = urllib3.PoolManager()
    html = pm.urlopen(url= main_url, method="GET").data
    soup = bs4.BeautifulSoup(html,'lxml')

    #La Jornada section format between 2007 and 2009
    if any(x for x in years07_09 if x in main_url) and 'jornada' in main_url:

        tag_list = soup.find_all(tag_type, class_= class_type)

        rel_links =[x['href'].strip('./') for x in tag_list if 'index' in x['href'] 
                    and 'impresa' not in x['href'] and 'edito' not in x['href'] and 
                    'correo' not in x['href'] and 'capital' not in x['href'] and 
                    'cartones' not in x['href'] and 'fotografia' not in x['href']]

        pattern = r'(\w*\.\w*\?\w*=)([a-z]+)'
        rel_links_menu = []

        for r in rel_links:
            rel = re.findall(pattern, r)

            if len(rel)>0 and (rel[0][1], main_url + r) not in rel_links_menu:
                rel_links_menu.append((rel[0][1], main_url + r))

        return rel_links_menu

    #La Jornada section format between 2010 and 2016    
    elif any(x for x in years10_16 if x in main_url) and 'jornada' in main_url:

        tag_list = soup.find_all(tag_type, class_ = class_type)[0]
        rel_links = tag_list.find_all('a')
        pattern = r'(?<=/)[a-z]+'
        rel_links_menu = []

        for r in rel_links:
            rel = re.findall(pattern, r['href'])
            if len(rel)>0 and (rel[0], main_url + rel[0]) not in rel_links_menu:
                rel_links_menu.append((rel[0], main_url + rel[0]))

        return rel_links_menu


    #La Jornada section format between 2017, LATimes section format
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

#jornada 07-09 tag-type = 'div'
#jornada 07-09 class_type ='article_list'
#jornada 10-16 tag_type = 'a'
#jornada 10-16 class_type = "cabeza"
#jornada tag_type = 'h4'
#latimes tag_type = 'h4'
#latimes class_type = 'trb_outfit_relatedListTitle'

def get_articles(sections_list, tag_type, class_type=None, original_url=None):
    '''
    Retrieve articles from every section in the 
    list of sections
    Inputs: A list of sections
            jornada 07-09 tag-type = 'div'
            jornada 07-09 class_type ='article_list'
            jornada 10-16 tag_type = 'a'
            jornada 10-16 class_type = "cabeza"
            jornada tag_type = 'h4'
            latimes tag_type = 'h4'
            latimes class_type = 'trb_outfit_relatedListTitle'

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
            #Tag list jornada articles 2007-2009
            if any(x for x in years07_09 if x in s) and 'jornada' in s:
                tag_list = soup.find_all(tag_type, id = class_type)
            #Tag list jornada articles 2010-2016
            elif any(x for x in years10_16 if x in s) and 'jornada' in s:
                tag_list = soup.find_all(tag_type, class_ = class_type)

            else:
                #Tag list LATimes articles 
                tag_list = soup.find_all(tag_type, class_ = class_type)
        else:
            tag_list = soup.find_all(tag_type)

        if original_url:
            if any(x for x in years07_09 if x in original_url) and 'jornada' in original_url:
                if len(tag_list)>0:
                    rel_list = tag_list[0].find_all('a')
                    for t in rel_list:
                        if 'index' in t['href']:
                            rel_article = t['href']
                            if key not in articles:
                                articles[key]= []
                            articles[key].append(original_url + rel_article)
            else:
                
                for t in tag_list:
                    rel_article = t['href']

                    if key not in articles:
                        articles[key]= []
                    articles[key].append(original_url + rel_article)

        else:    
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
            #sleep(randint(1,5))
            config = Configuration()
            config.browser_user_agent = get_user_agent()
            article = Article(i, language = 'es')
            article.download()
            if article.is_downloaded == True:
                article.parse()
                count = count + 1
                title = article.title
                print(title, key, count)
                date = article.publish_date
                text = article.text
                if key not in rv:
                    rv[key] = []
                rv[key].append((title, date, text))

    return rv
