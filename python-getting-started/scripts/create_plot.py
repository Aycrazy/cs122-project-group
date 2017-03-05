from hello.newsapp.models import Forum, Jornada
from scripts import create_date_range, get_date_ints, scatter_plot, histo_plot, time_series
import re



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

def run(*args):
