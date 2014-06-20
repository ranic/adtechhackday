from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'adsuggest.views.home', name='home'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'adsuggest/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^register$', 'adsuggest.views.register', name='register'),
)
