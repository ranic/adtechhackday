from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Route for built-in authentication with our own custom login page
    url(r'login$', 'django.contrib.auth.views.login', {'template_name':'adsuggest/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'register$', 'adsuggest.views.register', name='register'),
    url(r'share(?P<urlToShare>\S+)$', 'adsuggest.views.share', name='share'),
    url(r'referral(?P<id>\d+)$', 'adsuggest.views.referral', name='referral'),
    url(r'^like(?P<id>\d+)$', 'adsuggest.views.like', name='like'),
    url(r'^dislike(?P<id>\d+)$', 'adsuggest.views.dislike', name='dislike'),
    url(r'', 'adsuggest.views.home', name='home'),
)
