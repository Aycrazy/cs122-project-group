from hello.newsapp.models import ArticlesManager, Articles
from scripts import create_date_range, get_user_agent, get_articles, get_info, master_function
import re
import glob, os

#date_range will be a list of years provided by the user

#def create_db(date_range):

#re.findall(pattern, '2015/04/15')
#pattern = r'(?<=0)\d|\d{4}|[^0]\d*'
#result --> ['2015', '4', '15']

'''
def get_date_ints(article_dates):
    date_ints= None
    datetime_list = []
    pattern = r'(?<=0)\d|\d{4}|[^/0]\d*'
    for article_date in article_dates:
        date_ints = re.findall(pattern, article_date)
        y,m,d = date_ints
        datetime_list.append(datetime.date(int(y),int(m),int(d)))
    return datetime_list

def get_sentiment_info(keyword,date_range):
    '''
    #this will be run by the model to produce wanted output for sentiment analysis chart
    '''

    sentiment_list = []
    article_dates = []

    for date in date_range:
        sentiment = Jornada.objects.filter(title_contains=keyword, 'pub_date' = date)
        article_dates = sentiment.get_pub_date()
        datetime_list = get_date_ints(article_dates)
        article_dates.extend(date_datetime)
        sentiment_scores.append(sentiment.get_nltk_score())

    for date in date_range:
        sentiment = ProPublica.objects.filter(title_contains=keyword, 'pub_date' = date)
        article_dates = sentiment.get_pub_date()
        datetime_list = get_date_ints(article_dates)
        article_dates.extend(date_datetime)
        sentiment_scores.append(sentiment.get_nltk_score())


    return article_dates, sentiment_scores 

#keyword(string), date_range(list)
'''

def run(*args):
    os.chdir("/scripts")
    for file in glob.glob('*'+args[0]):
        with open(arg, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter='|')
            for row in csvreader
                article = Article.object.create_article(row['title'],row['pub_date'],\
                    row['nltk_score'],row['source'])

