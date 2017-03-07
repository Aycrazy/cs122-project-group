
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
from datetime import date, timedelta as td
import csv
from get_compound_scores import *
import mtranslate
import sys

# create_data_range ref from http://stackoverflow.com/questions/7274267/print-all-day-dates-between-two-dates

#main_url = "http://www.jornada.unam.mx/ultimas"
years07_09 = ['2007', '2008', '2009']
years10_17 = ['2010', '2011', '2012', '2013', '2014', '2015', '2016','2017']
visit = ['politica', 'economia', 'estados', 'sociedad', 'mundo', 'ciencias',
        'cultura']

#for the entire data scrape we will 2007,01,01 to 2012,12,31


def create_date_range(date1,date2):
    '''
    Will create a list of dates between given lower and upper date bounds
    Inputs:
        date1 = lower-bound date tuple
        date2 = upper-bound date tuple
    Outputs:
        date_list = list of dates between ranges
    '''
    y1,m1,d1 = date1
    y2,m2,d2 = date2

    d1 = date(y1, m1, d1)
    d2 = date(y2, m2, d2)

    delta = d2 - d1
    date_list = []

    for i in range(delta.days + 1):
         date_list.append(str(d1 + td(days=i)).replace('-','/'))
         
    return date_list

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
            jornada 10-17 tag_type = 'div'
            jornada 10-17 class_type = 'main-sections gui'
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
        if tag_list:
            rel_links =[x['href'].strip('./') for x in tag_list if 'index' in x['href'] 
                        and 'impresa' not in x['href'] and 'edito' not in x['href'] and 
                        'correo' not in x['href'] and 'capital' not in x['href'] and 
                        'cartones' not in x['href'] and 'fotografia' not in x['href']
                        and 'opinion' not in x['href'] and 'gastronomia' not in x['href']
                        and 'espectaculos' not in x['href'] and 'deportes' not in x['href']]

            pattern = r'(\w*\.\w*\?\w*=)([a-z]+)'
            rel_links_menu = []
            rel_links_menu = []

            for r in rel_links:
                rel = re.findall(pattern, r)

                if len(rel)>0 and (rel[0][1], main_url + r) not in rel_links_menu:
                    rel_links_menu.append((rel[0][1], main_url + r))

            return rel_links_menu
        else:
            return None

    #La Jornada section format between 2010 and 2016    
    elif any(x for x in years10_17 if x in main_url) and 'jornada' in main_url:

        tag_list = soup.find_all(tag_type, class_ = class_type)

        if tag_list:
            rel_links = tag_list[0].find_all('a')
            pattern = r'(?<=/)[a-z]+'
            rel_links_menu = []

            for r in rel_links:
                rel = re.findall(pattern, r['href'])
                if len(rel)>0 and (rel[0], main_url + rel[0]) not in rel_links_menu:
                    if rel[0] in visit:
                        rel_links_menu.append((rel[0], main_url + rel[0]))

            return rel_links_menu
        else:
            return None

    #La Jornada section format between 2017, LATimes section format
    tag_list = soup.find_all(tag_type, class_= class_type)
    if tag_list:
        rel_links_menu = []
        for t in tag_list: 
            pattern = r'(?<=/)[a-z]+'
            rel = re.findall(pattern, t.a['href'])

            if main_url == "www.latimes.com":
                if len(rel)>0 and (rel[0], main_url + '/' + rel[0]) not in rel_links_menu:
                    rel_links_menu.append((rel[1],main_url + '/'+rel[1]))
            elif len(rel)>1 and (rel[1], main_url + '/' + rel[1]) not in rel_links_menu:
                if rel[1] in visit:
                    rel_links_menu.append((rel[1],main_url + '/'+rel[1]))

        return rel_links_menu
    else:
        return None


#propublica tag_type = 'div'
#propublica class_type = 'excerpt-thumb'

def get_articles_pro(complement):
    '''
    '''
    propublica = 'https://www.propublica.org/archive/'
    archive_url = propublica +complement+'/'
    articles = {}
    pm = urllib3.PoolManager()
    html = pm.urlopen(url= archive_url, method="GET").data
    soup = bs4.BeautifulSoup(html, 'lxml')
    tag_list = soup.find_all('div', class_ = 'excerpt-thumb')

    if tag_list:
        for index,tag in enumerate(tag_list[0]):
            rv= {}
            articles[index] = rv
            article = tag.a['href']
            print(article)
            config = Configuration()
            config.browser_user_agent = get_user_agent()
            article_object = Article(article)
            article_object.download()
            if article_object:
                article_object.parse()
                title = article_object.title
                #date = article_object.publish_date
                text = article_object.text
                rv['article'] = title
                rv['pub_date'] = complement
                rv['nltk_score'] = get_nltk_score(text)
                rv['nltk_score_title'] =get_nltk_score(title)
                rv['source'] = 'ProPublica'

        write_csv_pro(articles, 'propublica_'+ re.sub("/", "_", complement) +'.csv')


    return articles

#jornada 07-09 tag-type = 'div'
#jornada 07-09 class_type ='article_list'
#jornada 10-16 tag_type = 'a'
#jornada 10-16 class_type = "cabeza"
#jornada tag_type = 'h4'


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
            elif any(x for x in years10_17 if x in s) and 'jornada' in s:
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
    count = 0
    for key, item in dictionary.items():
        #count = 0
        for i in item:
            #sleep(randint(1,5))
            config = Configuration()
            config.browser_user_agent = get_user_agent()
            article = Article(i, language = 'es')
            article.download()
            if article.is_downloaded == True:
                #rv['section'] = key
                irv = {}
                rv[count] = irv
                article.parse()
                count = count + 1
                title = article.title
                tr_title = mtranslate.translate(title, "en", "auto")
                #print(title, key, count)
                date = article.publish_date.date()
                text = article.text
                tr_text = translate_article(text)
                #if key not in rv:
                irv['article'] = title
                irv['pub_date'] = date
                irv['nltk_score'] = get_nltk_score(tr_text) #will be converted into sentiment score
                irv['source'] = 'Jornada'
                irv['nltk_score_title'] = get_nltk_score(tr_title)
                #rv[key].append((title, date, text))
    return rv

#Jornada Tags
#07-09 stag_type = 'a', sclass_type = 'visualIconPadding', atag_type = 'div', aclass_type = 'article_list'
#10-17 stag_type = 'div', sclass_type = 'main-sections gui', atag_type = 'a', aclass_type = 'cabeza'
#else stag_type = 'li', sclass_type = 'fixed-menu-p', atag_type = 'h4', aclass_type = None

def helper_funciton(main_url, stag_type,sclass_type, atag_type, aclass_type):
    sections_list = get_sections(main_url, stag_type, sclass_type)
    if sections_list:
        articles = get_articles(sections_list, atag_type, aclass_type, main_url)
        return get_info(articles)

def master_function(complement):
    '''
    '''
    #if 'jornada' in main_url:
    #    pattern = r'(.*.mx)(.*)'
    #    url_tuple = re.findall(pattern, main_url)[0]
    #    main, complement = url_tuple

    jornada = 'http://www.jornada.unam.mx/'
    main_url = jornada+complement+'/'
    #print(main_url)

    if any(x for x in years07_09 if x in complement): # and 'jornada' in main:
        #sections_list = get_sections(main_url, 'a', 'visualIconPadding')
        #articles = get_articles(sections_list, 'div', 'article_list', main_url)
        info_dictionary = helper_funciton(main_url,'a','visualIconPadding', 'div','article_list')
        if info_dictionary:
            write_csv(info_dictionary, 'jornada_'+ re.sub("/", "_", complement) +'.csv')
            return info_dictionary

    elif any(x for x in years10_17 if x in complement): # and 'jornada' in main:
        #sections_list = get_sections(main_url, 'div', 'main-sections gui')
        #articles = get_articles(sections_list, 'a', 'cabeza', main_url)
        #info_dictionary = get_info(articles)
        info_dictionary = helper_funciton(main_url,'div','main-sections gui', 'a','cabeza')
        if info_dictionary:
            write_csv(info_dictionary, 'jornada_'+ re.sub("/", "_", complement) +'.csv')
            return info_dictionary

    else:
        #sections_list = get_sections(main_url, 'li', 'fixed-menu-p')
        #articles = get_articles(sections_list, 'h4')
        info_dictionary = helper_funciton(main_url,'li','fixed-menu-p', 'h4', None)
        if info_dictionary:
            write_csv(info_dictionary, 'jornada_'+ re.sub("/", "_", complement) +'.csv')
            return info_dictionary

def downloader(start_date, end_date):
    '''
    Inputs:
        start_date "YYYY/MM/DD" (string)
        end_date "YYYY/MM/DD" (string)

    Outputs:
        csv_file (articles per day for the date range)
    '''
    date1 = start_date.split("/")
    y1, m1, d1 = (int(x) for x in date1)
    date2 = end_date.split("/")
    y2, m2, d2 = (int(x) for x in date2)
    date_range = create_date_range((y1, m1, d1), (y2, m2, d2))

    for day in date_range:
        master_function(day)
        get_articles_pro(day)

def write_csv(dictionary, filename):
    with open(filename, 'w') as csv_file:
        fieldnames = ['article','pub_date','nltk_score','source', 'nltk_score_title']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)#delimiter='|')
        writer.writeheader()
        for key, value in dictionary.items():
            #for i in dictionary[key]:
            writer.writerow(value)

def write_csv_pro(dictionary, filename):
    with open(filename, 'w') as csv_file:
        fieldnames = ['article','pub_date','nltk_score','source', 'nltk_score_title' ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)#delimiter='|')
        writer.writeheader()
        for value in dictionary.values():
            #for i in dictionary[key]:
            writer.writerow(value)

# if __name__ == "__main__":
#     # process arguments

#     if len(sys.argv) == 2:
#         start_date = sys.argv[0]
#         end_date = sys.argv[1]
#     else:
#         s = "usage: python3 <start_date tuple> <end_date tuple>"
#         print(s)
#         sys.exit(0)

#     downloader(start_date, end_date)