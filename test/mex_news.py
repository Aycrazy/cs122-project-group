
import urllib3
import bs4
import urllib.parse
import requests
import re





main_url = "http://www.jornada.unam.mx/ultimas"



def get_sections(main_url):
    '''
    '''
    pm = urllib3.PoolManager()
    html = pm.urlopen(url= main_url, method="GET").data
    soup = bs4.BeautifulSoup(html,'lxml')

    tag_list = soup.find_all('li', class_="fixed-menu-p")

    rel_links_menu = []
    for t in tag_list: 
        pattern = r'(?<=/)[a-z]+'
        rel = re.findall(pattern, t.a['href'])
        if len(rel)>1 and main_url + '/' + rel[1] not in rel_links_menu:
            rel_links_menu.append(main_url + '/'+rel[1])

    return rel_links_menu

def get_articles(sections_list):
    '''
    '''
    pm = urllib3.PoolManager()
    articles = []
    for s in sections_list:
        html = pm.urlopen(url= s, method="GET").data
        soup = bs4.BeautifulSoup(html, 'lxml')
        tag_list = soup.find_all('h4')
        for tag in tag_list:
            article = tag.a['href']

        articles.append(article)
    return articles
### GEt h4 tags
