from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from adsuggest.models import AdUser
from django.contrib.auth import login, authenticate

@login_required
def home(request):
    request.user.aduser.incrementScore()
    context = {'user' : request.user}
    return render(request, 'adsuggest/index.html', context)

@transaction.commit_on_success
def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'adsuggest/register.html', context)

    errors = []
    context['errors'] = errors

    # Checks the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
	errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['username'] = request.POST['username']

    if not 'password1' in request.POST or not request.POST['password1']:
	    errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
	    errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
	    errors.append('Passwords did not match.')

    if len(User.objects.filter(username = request.POST['username'])) > 0:
	    errors.append('Username is already taken.')

    if errors:
        return render(request, 'adsuggest/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'], \
                                        password=request.POST['password1'])
    new_user.save()
    new_ad_user = AdUser(user=new_user, score=0)
    new_ad_user.save()
    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=request.POST['username'], \
                            password=request.POST['password1'])
    login(request, new_user)
    return redirect('/adsuggest/')
