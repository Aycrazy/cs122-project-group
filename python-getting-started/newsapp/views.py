from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import requests
from scripts.financial_scraper import get_historical_stock, get_exchange_rate, get_historical_currency
from scripts.analysis import create_df, get_plots, scatter_plot_comparison
from .models import Article, Date, Ticker, Currency
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import date, timedelta
from scripts.form import UserInput
from scripts.translate import translate_keywords
import pandas as pd
import numpy as np
import random
import re

# Create your views here.
COLUMN_NAMES = [
        'Title',
        'Publish date',
        'Title Sentiment Score',
        'Text Sentiment Score',
        'Source',
]

def get_date_ints(article_date):
    pattern = r'(?<=0)\d|\d{4}|[^/0]\d*'
    date_ints = re.findall(pattern, article_date)
    #print(date_ints)
    m,d,y = date_ints
    return date(int(y),int(m),int(d))

def search_news(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = UserInput(request.POST)
        if form.is_valid():
            HttpResponse('Thank you we are processing your request')
    else:
        form = UserInput()
    return render(request,'search.html',{'form': form})

def results_png(dt,scores_text,scores_title,findata):

    df = create_df(dt,scores_text,scores_title,findata)

    get_plots(df)
    
    #return response

def results(request):
    context={}
    res=None
    startdate = date(int("2010"), int("01"), int("02"))
    dt = []
    while startdate < date(int("2010"), int("04"), int("10")):
        dt.append(startdate)
        startdate += timedelta(days=1)

    scores_text = [np.random.normal(0, 1) for i in range(len(dt))]
    scores_title = [np.random.normal(0, 1) for i in range(len(dt))]
    findata = [random.uniform(100, 300) for i in range(len(dt))]

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = UserInput(request.POST)

        # Check if the form is valid:
        if form.is_valid():

            args = True

            #findata=[]
            start_date = get_date_ints(form.data['start_date'])
            end_date = get_date_ints(form.data['end_date'])
            
            if form.data['home'] == 'United States':
                paper = 'ProPublica'
            else:
                paper = 'Jornada'

            #d = Article.objects.raw('SELECT * FROM ')

            if len(form.data['keyword'].split()) > 1:
                articles = d.article_set.filter(title__icontains=form.data['keyword'],source = paper)
                for word in form.data['keyword'].split()[1:]:
                    articles.filter(title__icontains=word+" ")
            else:
                articles = d.article_set.filter(title__icontains=form.data['keyword']+" ",source = paper)


            if form['stock_or_currency'] == 'stock':
                stocks = Ticker.objects.filter(ticker=form.data['ticker'], date__date_id__range=(start_date,end_date))
                for stock in stocks:
                    findata.append(stock.data['close'])
            else:
                home_rates = Currency.objects.filter( date__date_id__range=(start_date,end_date))
                for hr in home_rates:
                    findata.append(hr.data['currency'])


            #will need to filter these based on days there are articles
            

            

            demo_len = len(articles)
            print(len(articles))
            dates = []
            nltk_scores = []
            nltk_scores_title = []
            for article in articles:
                dates.append(article.date)
                nltk_scores.append(article.nltk_score)
                nltk_scores_title.append(article.nltk_score_title)


            

            res = articles
            #results_png(dt,scores_text,scores_title,findata)
            results_png(dates,nltk_scores,nltk_scores_title,findata[:demo_len])

            if not len(res):
                context['result'] = None
            else:
                context['result'] = res
                context['num_results'] = len(res)
                context['columns'] = COLUMN_NAMES
            context['form']=form
    else:
        form= UserInput()

    return render(request,'results.html',context)
'''
def index(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = UserInput(request.POST, initial= data)
        if form.is_valid():
            HttpResponse('Thank you we are processing your request')
    else:
        form = UserInput()
    #r = requests.get('http://httpbin.org/status/418')
    #print (r.text)

    return render(request,'index.html',{'form': form})

def db(request):

    return render(request, 'db.html')
'''