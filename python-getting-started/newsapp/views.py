from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import requests
from scripts.financial_scraper import get_historical_stock, get_exchange_rate, get_historical_currency #dict_to_csv
from .models import Article
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from scripts.forms import UserInput
# Create your views here.

def search_news(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = UserInput(request.POST, initial= data)
        if form.is_valid():
            HttpResponse('Thank you we are processing your request')
        else:
            form = UserInput()
    return render(request,'newsapp/templates/ssearch.html',{'form': form})

def results(request):

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = UserInput(request.POST, initial= data)

        if form.is_valid():

            # Check if the form is valid:

            if UserInput.stock_or_currency == 'stock':
                ticker = form.stock_choice()
                user_dict = get_historical_stock(form.start_date,form.end_date, ticker)

            #will need to filter these based on days there are articles
            

            if form.home == 'United States':
                paper = 'ProPublica'
            else:
                paper = 'Jornada'

            articles = Article.objects.filter(title__contains=form.keyword,pub_date__range=(form.start_date,form.end_date),source = paper)
            
            dates = []
            nltk_scores = []

            for article in articles:
                dates.append(article.pub_date)
                nltk_scores.append(article.nltk_score)

            c_or_s_list = [v for k,v in user_dict.items() if k in dates]
    else:
        form= UserInput()
        # 

    #    if Currency.objects.filter(ticker=form.choose_stock,date=):
    #        Currency.
        #if date is a weekend choose Friday of that week
        
        #call get_historical stock with date ranges and selected ticker
        #turn dictionary close into list

    #for dates chosen and newspaper source
        #query ARTICLE table and get relevant articles with all info
            #if there are multiple articles for a keyword for that day -average the sentiment
            #else just use the sentiment for the one article
            #make a list of dates
    return render(request,'newsapp/templates/results.html')

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

    return render(request,'newsapp/templates/index.html',{'form': form})

def db(request):

    return render(request, 'db.html')