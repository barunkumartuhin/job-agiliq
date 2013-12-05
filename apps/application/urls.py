from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^authorize/', 'apps.application.views.authorize', name='test'),
    url(r'^access_token/', 'apps.application.views.get_access_token', name='access_token'),
    url(r'^upload/', 'apps.application.views.upload_resume', name='upload'),
)