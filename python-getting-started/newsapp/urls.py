from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from . import views 

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),
#app_name = 'newsapp'
urlpatterns = [
    #url(r'^index', views.index, name='index'),
    #url(r'^db', views.db, name='db'),
    url(r'^search',views.search_news, name ='search'),
    url(r'^results', views.results, name='results'),
]
