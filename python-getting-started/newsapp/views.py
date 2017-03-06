from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import requests
from scripts.financial_scraper import get_historical_stock, get_exchange_rate, get_historical_currency #dict_to_csv
from .models import Article,Currency, Ticker
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from .forms UserInput
# Create your views here.

def my_view(request):

    # If this is a POST request then process the Form data
    if request.method = 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = UserInput(request.POST)

        # Check if the form is valid:
        
    if form.stock_or_currency = 'currency':
    #    if Currency.objects.filter(ticker=form.choose_stock,date=):
    #        Currency.
        #if date is a weekend choose Friday of that week
        
        #call get_historical stock with date ranges and selected ticker
        #load dictionary into currency sql? (maybe if necessary)
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