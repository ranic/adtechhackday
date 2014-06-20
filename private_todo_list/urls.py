from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'private_todo_list.views.home', name='home'),
    url(r'^add-item', 'private_todo_list.views.add_item', name='add'),
    url(r'^delete-item/(?P<id>\d+)$', 'private_todo_list.views.delete_item', name='delete'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'private-todo-list/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^register$', 'private_todo_list.views.register', name='register'),
)
