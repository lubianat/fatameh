from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import pprint, os
from wikidataintegrator import wdi_core, wdi_login, wdi_helpers
from requests_oauthlib import OAuth1
from django.conf import settings



def index(request):
    context = {}
    return render(request, 'add_paper/index.dtl', context)

@login_required()
def profile(request):
    context = {}
    return render(request,'add_paper/profile.dtl', context)

def login_oauth(request):
    context = {}
    return render(request, 'add_paper/login.dtl', context)

@login_required()
def add(request, item):
    context = {}
    social = request.user.social_auth.get(provider="mediawiki")
    token = social.extra_data['access_token']['oauth_token']
    usersecret = social.extra_data['access_token']['oauth_token_secret']
    mediawiki_key = settings.SOCIAL_AUTH_MEDIAWIKI_KEY
    mediawiki_secret = settings.SOCIAL_AUTH_MEDIAWIKI_SECRET
    login_instance = wdi_login.WDLogin(consumer_key=mediawiki_key,
                                       consumer_secret=mediawiki_secret)
    login_instance.s.auth = OAuth1(mediawiki_key,
                                   client_secret=mediawiki_secret,
                                   resource_owner_key=token,
                                   resource_owner_secret=usersecret)
    login_instance.generate_edit_credentials()
    item=wdi_helpers.PubmedItem(item)
    return JsonResponse({"item": item.get_or_create(login_instance)})
