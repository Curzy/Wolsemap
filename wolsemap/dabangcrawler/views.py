import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from dabangcrawler.models import Station


class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='wolsemap.html')


class WolseMapView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='wolsemap.html')


class StationListView(generic.View):
    def get(self, request, *args, **kwargs):
        stations = [dict(
            value=station.dabang_id,
            label=' '.join(
                [station.name] +
                [line.name
                 for line in station.line.order_by()]
            )
        ) for station in Station.objects.all()]

        return HttpResponse(json.dumps(stations))


class StationRecordView(generic.View):
    def get(self, request, station_id, *args, **kwargs):
        station_record = dict()
        if station_id:
            station = Station.objects.get(dabang_id=station_id)
            lines = station.line.order_by().values_list('name', flat=True)
            price_history = [
                dict(date=price['created_at'].strftime('%Y-%m-%d'),
                     deposit=price['deposit'],
                     price=price['price'])
                for price in station.price_history.values(
                    'deposit', 'price', 'created_at'
                ).order_by('-created_at')
            ]
            station_record = dict(
                id=station.dabang_id,
                name=station.name,
                line=list(lines),
                price_history=price_history,
            )
            return HttpResponse(json.dumps(station_record))
