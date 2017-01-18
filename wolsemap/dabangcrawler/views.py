import json

from django.db.models import Avg
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Station


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
        if station_id:
            station = Station.objects.get(dabang_id=station_id)
            lines = station.line.order_by().values_list('name', flat=True)
            price_history = [
                dict(date=date,
                     deposit=deposit,
                     price=price)
                for date, deposit, price in station.price_history.extra(
                    select={'created_date': 'DATE(created_at)'}
                ).annotate(Avg('deposit'), Avg('price')).values_list(
                    'created_date', 'deposit__avg', 'price__avg'
                ).order_by('-created_at')
            ]
            station_record = dict(
                id=station.dabang_id,
                name=station.name,
                line=list(lines),
                price_history=price_history,
            )
            return HttpResponse(json.dumps(station_record))
