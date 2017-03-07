from django.conf.urls import include, url
#from . import newsapp
from django.contrib import admin
admin.autodiscover()

#from . import newsapp.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),
#app_name = 'newsapp'

urlpatterns = [
    url(r'^', include('newsapp.urls')),
    url(r'^admin/', admin.site.urls)
]