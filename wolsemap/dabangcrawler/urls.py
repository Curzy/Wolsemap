__author__ = 'Curzy'

from django.conf.urls import url
from .views import WolseMapView, IndexView, StationRecordView, StationListView

app_name = 'wolsemap'
urlpatterns =[
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^wolsemap/$', WolseMapView.as_view(), name='wolsemap'),
    url(r'^wolsemap/stations/$', StationListView.as_view(), name='station_list'),
    url(r'^wolsemap/station/(\d+)/$', StationRecordView.as_view(), name='station_record'),
]
