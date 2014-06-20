from django import forms
from adsuggest.models import AdUser, Ad, SharedAd, LONG

class ShareForm(forms.Form):
    email = forms.CharField(max_length=LONG, widget=forms.TextInput(attrs={'placeholder': 'Enter your friend\'s email'}))
