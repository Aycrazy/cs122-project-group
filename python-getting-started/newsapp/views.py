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

def search_news_sentiment(request):

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = UserInput(request.POST)

        # Check if the form is valid:

        if UserInput.stock_or_currency == 'stock':
            ticker = form.stock_choice()
            user_dict = get_historical_stock(form.start_date,form.end_date, ticker)

        user_list = [for v in user_dict.values()]

        if form.home == 'United States':
            source = 'ProPublica'
        else:
            source = 'Jornada'

        Article.objects.filter(pub_date__range=(form.start_date,form.end_date),)
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
    pass

def index(request):
    #r = requests.get('http://httpbin.org/status/418')
    #print (r.text)

    return render(request,'index.html')

def db(request):

    return render(request, 'db.html')