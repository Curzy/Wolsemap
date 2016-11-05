import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from dabangcrawler.models import Station, Price


class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='index.html')


class WolseMapView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='wolsemap.html')


class StationListView(generic.View):
    def get(self, request, *args, **kwargs):
        stations = [dict(value=station.dabang_id, label=' '.join([station.name] + [line.lines for line in station.line.order_by()])) for station in Station.objects.all()]
        return HttpResponse(json.dumps(stations))


class StationRecordView(generic.View):
    def get(self, request, station_id, *args, **kwargs):
        station_record = dict()
        if station_id:
            station = Station.objects.get(dabang_id=station_id)
            lines = station.line.order_by().values_list('lines', flat=True)
            price_history = [
                dict(
                    date=station['created_at'].strftime('%Y-%m-%d'),
                    deposit=station['deposit'],
                    price=station['price']
                )
                for station in station.price_history.order_by('-created_at').values('deposit', 'price', 'created_at')
            ]
            station_record = dict(
                id=station.dabang_id,
                name=station.name,
                line=list(lines),
                price_history=price_history,
            )
            return HttpResponse(json.dumps(station_record))
