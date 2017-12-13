from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import pprint, os
from wikidataintegrator import wdi_core, wdi_login, wdi_helpers
from requests_oauthlib import OAuth1
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view



def index(request):
    context = {}
    return render(request, 'add_paper/index.dtl', context)

@login_required()
def profile(request):
    context = {
        'token': Token.objects.get_or_create(user=request.user)[0]
    }
    print(Token.objects.get_or_create(user=request.user))
    return render(request,'add_paper/profile.dtl', context)

def login_oauth(request):
    context = {}
    return render(request, 'add_paper/login.dtl', context)



def add(request, item, type="MED"):
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
    item=wdi_helpers.PubmedItem(item, id_type=type)
    item_string=item.get_or_create(login_instance)
    print(item.errors)
    return JsonResponse({"item": item_string, "error": item.errors})

@login_required()
def addPMID(request, item):
    return add(request, item)

@login_required()
def addPMCID(request, item):
    return add(request, item, type="PMC")

@api_view(['GET'])
def tokenAddPMCID(request, item):
    return add(request, item, type="PMC")

@api_view(['GET'])
def tokenAddPMID(request, item):
    return add(request, item)