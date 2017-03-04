from hello.newsapp.models import Forum, Jornada
from scripts import get_user_agent, get_articles, get_info, master_function
import re

#date_range will be a list of years provided by the user

#def create_db(date_range):

#re.findall(pattern, '2015/04/15')
#pattern = r'(?<=0)\d|\d{4}|[^0]\d*'
#result --> ['2015', '4', '15']



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
    this will be run by the model to produce wanted output for sentiment analysis chart
    '''

    sentiment_list = []
    article_dates = []

    for date in date_range:
        sentiment = Jornada.objects.filter(title_contains=keyword, 'pub_date' = date)
        article_dates = sentiment.get_pub_date()
        datetime_list = get_date_ints(article_dates)
        article_dates.extend(date_datetime)
        sentiment_scores.append(sentiment.get_nltk_score())

    return article_dates, sentiment_scores 

#keyword(string), date_range(list)

def run(*args):

    article_date, sentiment_score = get_sentiment_info(args[0],args[1])

    for a in range(len(article_date)):
        #plot?
    #Fetches necessary information from user
