
import urllib3
import bs4
import urllib.parse
import requests
import re
from io import StringIO
import newspaper
from newspaper import Article
import pandas as pd
import csv
import numpy as np
import queue
import datetime

ref1 = 'http://pqasb.pqarchiver.com/latimes/results.html?st=advanced&QryTxt=White+House&type=current&sortby=CHRON&datetype=0&frommonth=01&fromday=01&fromyear=1985&tomonth=02&today=08&toyear=2017&By=&Title=&at_curr=ALL&Sect=ALL'

'''
ref2 =http://pqasb.pqarchiver.com/<SOURCE>/results.html?st=advanced&QryTxt=<text1>+<text2>+...<textN>&type=current&sortby=CHRON&datetype=0&frommonth=<MONTH # FROM>&fromday=<DAY # FROM>&fromyear=<YEAR # FROM>&tomonth=<MONTH # TO>&today=<DAY # TO>&toyear=<YEAR # TO>&By=&Title=&at_curr=ALL&Sect=ALL
'''



def get_input(source, text, from_month, from_day, from_year, to_month, to_day, to_year):

    text_split = text.split()[0]

    archive_url = 'http://pqasb.pqarchiver.com/'+source+'/results.html?st=advanced&QryTxt='\
    +text_split+'&type=current&sortby=CHRON&datetype=0&frommonth='\
    +'&frommonth='+from_month+'&fromday='+from_day+'&fromyear='+from_year+'&tomonth='+'&today='+to_day+'&toyear='+to_year+\
    '&By=&Title=&at_curr=ALL&Sect=ALL' #need to fix text part for multiple text input

    return archive_url


def get_archive_articles(archive_url, tag_type, class_type):
    '''
    Find all the articles in the newspaper
    Inputs: main url 
    Returns: A list with the links for all the sections
    '''
    pm = urllib3.PoolManager()
    html = pm.urlopen(url= archive_url, method="GET").data
    soup = bs4.BeautifulSoup(html,'lxml')

    tag_list = soup.find_all('td', class_= 'top')

    return soup, [tag.a['href'] for tag in tag_list]

def get_next_page(archive_url):

    catalog = queue.Queue()
    pm = urllib3.PoolManager()
    html = pm.urlopen(url= archive_url, method="GET").data
    soup = bs4.BeautifulSoup(html,'lxml')
    print(soup)
    a_tag = soup.find_all('a')
    print(a_tag[0])
    span_tag = soup.find_all('span', class_='resultsheader')
    print(span_tag)
    pre = 'http://pqasb.pqarchiver.com/latimes/'

    soup_section = bs4.BeautifulSoup(span_tag[0],lxml)
    next_pages = soup_section.find_all('a',class_='resultsheader')
    for np in next_pages:
        whole = pre+np
        catalog.add(whole)

    return catalog


 #div, class_='resultpgs' ,a, href   

def get_user_agent():
    '''
    '''
    user_agents = []

    usertext = pd.read_table('newspaper/resources/misc/useragents.txt',sep='*', header=None)

    stacked = usertext.stack()

    pd.set_option('display.width', 1000)

    return stacked.sample(1).reset_index()[0][0].strip(' ')

    return d