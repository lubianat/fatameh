from django.conf.urls import url, include
from add_paper import views

urlpatterns = [
    url(r'^profile$', views.profile, name='profile'),
    url(r'^accounts/login$', views.login_oauth, name='login'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^pmc/add/(?P<item>PMC[0-9]+$)', views.addPMCID),
    url(r'^token/pmc/add/(?P<item>PMC[0-9]+$)', views.tokenAddPMCID),
    url(r'^token/pmid/add/(?P<item>[0-9]+$)', views.tokenAddPMID),
    url(r'', views.index),
]
