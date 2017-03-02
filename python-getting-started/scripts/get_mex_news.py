from hello.newsapp.models import Forum, Jornada

#date_range will be a list of years provided by the user

def get_sentiment_info(keyword,date_range):
    sentiment_list = []
    article_dates = []

    for date in date_range:
        sentiment = Jornada('name' =keyword, 'pub_date = date)
        article_dates.append(sentiment.get_pub_date())
        sentiment_scores.append(sentiment.get_nltk_score())

    return article_dates, sentiment_scores 

def run(keyword,date_range):
    article_date, sentiment_score = get_sentiment_info()

    for a in range(len(article_date)):
        #plot?
    #Fetches necessary information from user
