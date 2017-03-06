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
    url(r'^search/(?P,pk.[-\w]+)/news_sentiment/$', newsapp.views.my_view, name='search_news_sentiment')
]
