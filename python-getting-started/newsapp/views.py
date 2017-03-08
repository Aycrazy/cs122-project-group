from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import requests
from scripts.financial_scraper import get_historical_stock, get_exchange_rate, get_historical_currency
from scripts.analysis import create_df, get_plots
from .models import Article, Ticker, Currency
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from scripts.form import UserInput
import pandas as pd

# Create your views here.

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

    response = get_plots(df)

    return response

def results(request):

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
            findata=[]
            if form.stock_or_currency == 'stock':
                #stocks = Ticker.objects.filter(ticker=form.ticker, date__range(form.start_date,form.end_date))
                for stock in stocks:
                    findata.append(stock.close)
            else:
                #home_rates = Currency.objects.filter(country=form.home, date__range(form.start_date,form.end_date))
                for hr in home_rates:
                    findata.append(hr.currency)


            #will need to filter these based on days there are articles
            

            if form.home == 'United States':
                paper = 'ProPublica'
            else:
                paper = 'Jornada'

            articles = Article.objects.filter(title__contains=form.keyword,pub_date__range=(form.start_date,form.end_date),source = paper)
            

            dates = []
            nltk_scores = []
            nltk_scores_title = []
            for article in articles:
                dates.append(article.pub_date)
                nltk_scores.append(article.nltk_score)
                nltk_scores_title.append(article.nltk_score_title)

            results_png(dt,scores_text,scores_title,findata)

    else:
        form= UserInput()

    return render(request,'results.html')

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