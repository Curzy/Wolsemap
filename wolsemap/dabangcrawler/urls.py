__author__ = 'Curzy'

from django.conf.urls import include, url
from . import views

urlpatterns =[
    url(r'^$', views.wolsemap, name='wolsemap')
]