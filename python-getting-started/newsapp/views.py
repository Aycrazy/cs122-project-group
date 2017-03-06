from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import requests
#from .models import Greeting

# Create your views here.
def my_view(request):
    pass

def index(request):
    #r = requests.get('http://httpbin.org/status/418')
    #print (r.text)

    return render(request,'index.html')

def db(request):

    return render(request, 'db.html')
