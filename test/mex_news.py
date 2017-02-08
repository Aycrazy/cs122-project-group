
import urllib3
import bs4
import urllib.parse
import requests
import re
from io import StringIO
import newspaper
from newspaper import Article


main_url = "http://www.jornada.unam.mx/ultimas"



def get_sections(main_url):
    '''
    Find all the sections in the newspaper
    Inputs: main url 
    Returns: A list with the links for all the sections
    '''
    pm = urllib3.PoolManager()
    html = pm.urlopen(url= main_url, method="GET").data
    soup = bs4.BeautifulSoup(html,'lxml')

    tag_list = soup.find_all('li', class_="fixed-menu-p")

    rel_links_menu = []
    for t in tag_list: 
        pattern = r'(?<=/)[a-z]+'
        rel = re.findall(pattern, t.a['href'])
        if len(rel)>1 and (rel[1], main_url + '/' + rel[1]) not in rel_links_menu:
            rel_links_menu.append((rel[1],main_url + '/'+rel[1]))

    return rel_links_menu

def get_articles(sections_list):
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
        tag_list = soup.find_all('h4')
        
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
            article = Article(i, language = 'es')
            article.download()
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