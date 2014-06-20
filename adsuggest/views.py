from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


def home(request):
    return render(request, 'adsuggest/index.html', {})


