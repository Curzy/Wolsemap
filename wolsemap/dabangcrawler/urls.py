__author__ = 'Curzy'

from django.conf.urls import url
from .views import WolseMapView, IndexView

app_name = 'wolsemap'
urlpatterns =[
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^wolsemap/$', WolseMapView.as_view(), name='wolsemap')
]