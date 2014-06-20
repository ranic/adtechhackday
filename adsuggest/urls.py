from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'adsuggest.views.home', name='home'),
)
