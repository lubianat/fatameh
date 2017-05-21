from django.conf.urls import url, include
from add_paper import views

urlpatterns = [
    url(r'profile', views.profile, name='profile'),
    url(r'accounts/login', views.login_oauth, name='login'),
    url(r'oauth/', include('social_django.urls', namespace='social')),
    url(r'add/(?P<item>[0-9]+)', views.add),
    url(r'', views.index),
]
