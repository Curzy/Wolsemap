from __future__ import absolute_import
import json
import time

from urllib.request import Request, urlopen

from .models import Line, Station
from .tasks import crawl_dabang
from concurrent.futures import ThreadPoolExecutor, as_completed


def preset_subway_lines():
    Line.objects.all().delete()
    subway_lines = ('1호선', '2호선', '3호선', '4호선', '5호선', '6호선',
                    '7호선', '8호선', '9호선', '분당선', '신분당선', '경의선',
                    '중앙선', '공항철도', '용인에버라인')

    for line_name in subway_lines:
        Line.objects.create(name=line_name)


def insert_stations(station_id_start, station_id_end):
    Station.objects.all().delete()

    start = time.time()

    station_price_dict = {}

    with ThreadPoolExecutor(max_workers=15) as executor:
        future_to_id = dict(
            (executor.submit(crawl_dabang, station_id, 1), station_id)
            for station_id in range(station_id_start, station_id_end)
        )
        for future in as_completed(future_to_id):
            station_id = future_to_id[future]
            try:
                station_info = future.result()
                if station_info:
                    station_price_dict[station_id] = station_info
            except Exception as e:
                print(f'station id : {station_id} generated an exception: {e}')

    for station_id in list(station_price_dict.keys()):
        station_info = station_price_dict[station_id]

        station_name = station_info['subway']['name']
        station_lines = station_info['subway']['line']

        station_object = Station.objects.create(dabang_id=station_id,
                                                name=station_name)
        for line in station_lines:
            try:
                line = Line.objects.get(name=line)
                station_object.station_lines.add(line)
                station_object.save()
            except Exception as e:
                print(f'station id : {station_id} generated an exception: {e}')
        print(station_id, station_name, station_lines)

    duration = time.time() - start
    print('Station db set time :', duration)


def get_zigbang_stations():
    url = 'https://api.zigbang.com/v1/search/subway?q='

    request = Request(url)
    response = urlopen(request)

    station_data = json.loads(response.read())

    return station_data


def insert_station_coordinate():
    stations = get_zigbang_stations()

    for station in stations:
        name = station['name']
        latitude = station['location'][0]
        longitude = station['location'][1]

        Station.objects.filter(name=name).update(latitude=latitude,
                                                 longitude=longitude)
