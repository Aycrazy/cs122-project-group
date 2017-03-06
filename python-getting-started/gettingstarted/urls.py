from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import newsapp.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),
app_name = 'newsapp'
urlpatterns = [
    url(r'^index', newsapp.views.index, name='index'),
    url(r'^db', newsapp.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search_news_sentiment/$', newsapp.views.search_news_sentiment, name='search_news_sentiment')
]
