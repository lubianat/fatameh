from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    context = {}
    return render(request, 'add_paper/index.dtl', context)

@login_required()
def profile(request):
    contect = {}
    return render(request,'add_paper/profile.dtl', context)

def login_oauth(request):
    context = {}
    return render(request, 'add_paper/login.dtl', context)
