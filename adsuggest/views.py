from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.core.mail import send_mail

# Used to create and manually log in a user
from django.contrib.auth.models import User
from adsuggest.models import AdUser, Ad, SharedAd
from django.contrib.auth import login, authenticate
from adsuggest.forms import ShareForm
from random import randint

def getAd(user):
    #TODO: Make this more intelligent than just randomly selecting an ad
    allAds = Ad.objects.all()
    return allAds[randint(0, len(allAds)-1)]
    

@login_required
def home(request):
    ad = getAd(request.user.aduser)
    embedUrl = ad.embedUrl()
    context = {'user' : request.user, 'form' : ShareForm(), 'ad': ad, 'embedUrl' : embedUrl}
    return render(request, 'adsuggest/index.html', context)


@login_required
def share(request, urlToShare):
    context = {}
    context['errors'] = []
    if request.method=="POST":
        print "Url to share is: %s" % urlToShare
        form = ShareForm(request.POST)
        if not form.is_valid():
            context['form'] = form
            return render(request, 'adsuggest/index.html', context)
        sent_by = request.user.aduser
        sent_to = get_object_or_404(User, username=form.cleaned_data.get('email')).aduser
        ad = get_object_or_404(Ad, url_id=urlToShare)
        sharedAdObj = SharedAd(sent_by=sent_by, sent_to=sent_to, ad=ad, url="")
        sharedAdObj.save()
        customUrl = "localhost:8000/adsuggest/referral%d" % sharedAdObj.pk
        sharedAdObj.url = customUrl
        sharedAdObj.save()
        send_mail(subject="You got a video referral!",
                  message="%s thought you might enjoy this ad: %s. \n If you do, let us know and you'll get more like this in the future." % (sent_by.user.username, customUrl),
                  from_email="vijay+devnull@andrew.cmu.edu",
                  recipient_list=[sent_to.user.username])
        messages.add_message(request, messages.INFO, "Successfully referred video to %s. If they like it, you'll get a point. If they dislike it, you'll lose a point." % sent_to.user.username)
    return redirect('/adsuggest/index.html')

@login_required
def referral(request, id):
    sharedAdObj = SharedAd.objects.get(pk=id)
    if (request.user != sharedAdObj.sent_to.user):
        messages.add_message(request, messages.INFO, "You were not authorized to view that page, so we redirected you.")
        return redirect('/adsuggest/index.html')
    
    ad = sharedAdObj.ad
    context = {'embedUrl' : ad.embedUrl(), 'sent_by' : sharedAdObj.sent_by.user, 'ad' : ad, 'id' : sharedAdObj.pk}
    context['is_liked'] = sharedAdObj.is_liked
    context['is_disliked'] = sharedAdObj.is_disliked
    context['form'] = ShareForm()
    return render(request, 'adsuggest/referral.html', context)

@login_required
def like(request, id):
    context = {}
    sharedAdObj = SharedAd.objects.get(pk=id)
    if (request.user != sharedAdObj.sent_to.user):
        messages.add_message(request, messages.INFO, "You were not authorized to view that page, so we redirected you.")
        return redirect('/adsuggest/index.html')
    print "calling like function"
    sharedAdObj.like()
 
    return redirect(request.META['HTTP_REFERER'])

@login_required
def dislike(request, id):
    context = {}
    sharedAdObj = SharedAd.objects.get(pk=id)
    if (request.user != sharedAdObj.sent_to.user):
        messages.add_message(request, messages.INFO, "You were not authorized to view that page, so we redirected you.")
        return redirect('/adsuggest/index.html')
    print "calling dislike function"
    sharedAdObj.dislike()
 
    return redirect(request.META['HTTP_REFERER'])

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
