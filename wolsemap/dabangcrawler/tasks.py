# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import json
import zlib
import datetime

from celery import shared_task
from django.conf import settings
from django.db.models import Avg

from .models import Station, Price
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.parse import urljoin

PROJECT_PATH = settings.PROJECT_PATH


def crawl_dabang(station_id, page_number):
    # 방 종류 list로 / 0: 원룸, 1: 1.5룸,
    # 2: 투룸, 3: 쓰리룸, 4: 오피스텔, 5: 아파트
    # 검색조건 room-type 0 = 월세만, deposit-range 보증금,
    # price-range 범위, room-size 5평 - 10평 사이
    room_type = [0]
    room_size_min = 16
    room_size_max = 33
    deposit_min = 0
    deposit_max = 5000
    price_min = 10
    price_max = 999999

    base_url = 'http://www.dabangapp.com/api/2/room/list/'
    station_page = f'subway?id={station_id}&page={page_number}'
    filters = (
        f'&filters={{"room-type":{room_type},'
        f'"room-size":[{room_size_min},{room_size_max}],'
        f'"deposit-range":[{deposit_min},{deposit_max}],'
        f'"price-range":[{price_min},{price_max}]}}'
    )

    url = urljoin(base_url, ''.join([station_page, filters]))
    request = Request(url, headers={'Accept-Encoding': 'gzip'})
    response = urlopen(request)
    dump = zlib.decompress(response.read(), 47).decode('utf-8')
    station_data = json.loads(dump)
    response.close()

    return station_data if validate_station(station_data) else False


def validate_station(station):
    in_seoul = station_in_seoul_subway(station)
    has_room = station_has_room(station)

    return in_seoul and has_room


def station_in_seoul_subway(station):
    subway_lines = ('1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선',
                    '8호선', '9호선', '분당선', '신분당선', '경의선', '중앙선',
                    '공항철도', '용인에버라인')
    subway_line = station['subway']['line']
    if not subway_line:
        return False
    elif subway_line[0] not in subway_lines:
        return False
    else:
        return True


def station_has_room(station):
    total_room = station['total']

    return total_room != 0


def dabang_averaging(station_info):
    """각 역의 검색 결과에서 방들의 보증금과 월세를 평균낸다"""
    total_deposit = 0
    total_price = 0
    total_rooms = 0

    station_name = station_info['subway']['name']
    subway_line = station_info['subway']['line']

    while True:
        for room in station_info['rooms']:

            room_deposit = room['price_info'][0][0]
            total_deposit += room_deposit

            room_price = room['price_info'][0][1]
            total_price += room_price

            total_rooms += 1

        has_more = station_info['has-more']
        if has_more:
            station_info = crawl_dabang(
                station_info['subway']['id'],
                station_info['next-page']
            )
        else:
            break

    average_deposit = total_deposit / total_rooms

    average_price = total_price / total_rooms

    return station_name, subway_line, average_deposit, average_price


@shared_task
def insert_price(station_id):
    crawled = crawl_dabang(station_id, page_number=1)
    if crawled:
        average = dabang_averaging(crawled)
        deposit = average[2]
        price = average[3]
        station = Station.objects.get(dabang_id=station_id)
        price_object = Price.objects.create(
            station=station, deposit=deposit,
            price=price, source=Price.SOURCE_DABANG)
        print(str(station_id) + ' ' + str(price_object.station.name) + ' '
              + str(price_object.deposit) + '/' + str(price_object.price) + ' '
              + str(price_object.get_source_display()))
        return (price_object.station.name,
                price_object.deposit,
                price_object.price)


@shared_task
def insert_prices(station_id_start, station_id_end):

    with ThreadPoolExecutor(max_workers=15) as executor:
        future_to_id = dict(
            (executor.submit(insert_price, station_id), station_id)
            for station_id in range(station_id_start, station_id_end)
        )
        for future in as_completed(future_to_id):
            station_id = future_to_id[future]
            try:
                future.result()
            except Exception as e:
                print(f'station id : {station_id} generated an exception: {e}')

    zigbang_coordinates = get_zigbang_coordinates()
    with ThreadPoolExecutor(max_workers=15) as executor:
        future_to_id = dict(
            (executor.submit(
                insert_zigbang_price,
                *[
                    station_id,
                    zigbang_coordinates.get(station_id, dict()).get('latitude'),
                    zigbang_coordinates.get(station_id, dict()).get('longitude')
                ]
            ), station_id)
            for station_id in range(station_id_start, station_id_end)
        )
        for future in as_completed(future_to_id):
            station_id = future_to_id[future]
            try:
                future.result()
            except Exception as e:
                print(f'station id : {station_id} generated an exception: {e}')

    with open(
        os.path.join(
            PROJECT_PATH,
            'dabangcrawler/maps/Seoul_subway_linemap_ko.svg'
        ), 'r'
    ) as original_map_f:
        with open(
            os.path.join(
                PROJECT_PATH,
                'dabangcrawler/static/svg/price_inserted_subway_linemap.svg'
            ), 'w'
        ) as subway_price_map_f:
            price_to_map(original_map_f, subway_price_map_f)


@shared_task
def price_to_map(original_subway_map, subway_price_map):
    original_map = original_subway_map.read()
    recent_prices = Price.objects.filter(
        created_at__gte=datetime.date.today()
    ).values('station').annotate(
        Avg('deposit'), Avg('price')
    ).values_list('station__name', 'deposit__avg', 'price__avg')

    for station_name, deposit, price in recent_prices:
        station_name_without_yeok = station_name[0:-1]

        deposit = int(round(deposit, -2))
        price = int(round(price, -1))

        station_price = str(deposit) + "/" + str(price)

        name_with_price = station_name_without_yeok + ' ' + station_price

        original_map = original_map.replace(
            '>' + station_name_without_yeok + '<', '>' + name_with_price + '<'
        )

    subway_price_map.write(original_map)
    os.system('echo yes | python manage.py collectstatic')

    return True


def get_zigbang_stations():
    url = 'https://api.zigbang.com/v1/search/subway?q='

    request = Request(url)
    response = urlopen(request)

    station_data = json.loads(response.read())

    return station_data


def get_zigbang_room_ids(latitude, longitude):
    # 방 종류 / 01: 원룸 오픈형, 02: 원룸 분리형, 03: 원룸 복층형, 04: 투룸, 05: 쓰리룸
    # deposit, rent _s, _e 최소, 최대
    room = '01;02;03'
    deposit_e = 5000
    rent_s = 10

    lat_difference = 0.0153
    lng_difference = 0.0277

    lat_south = latitude - lat_difference
    lat_north = latitude + lat_difference

    lng_west = longitude - lng_difference
    lng_east = longitude + lng_difference

    base_url = 'http://api.zigbang.com/v2/'
    parameters = (
        f'items?lat_south={lat_south}&lat_north={lat_north}&'
        f'lng_west={lng_west}&lng_east={lng_east}&'
        f'room={room}&deposit_e={deposit_e}&rent_s={rent_s}'
    )

    url = urljoin(base_url, parameters)

    request = Request(url)
    response = urlopen(request)
    data = json.loads(response.read())

    items = data['list_items']

    item_ids = [item['simple_item']['item_id'] for item in items]

    return item_ids


def get_zigbang_coordinates():

    station_coordinates = dict()
    for dabang_id, latitude, longitude in Station.objects.values_list(
            'dabang_id', 'latitude', 'longitude'):
        station_coordinates[dabang_id] = dict(latitude=latitude,
                                              longitude=longitude)

    return station_coordinates


def crawl_zigbang(latitude, longitude):
    base_url = 'http://api.zigbang.com/v1/'
    base_parameter = 'items?detail=true&'
    item_ids = get_zigbang_room_ids(latitude, longitude)
    item_id_chunks = [item_ids[i: i + 60]
                      for i in range(0, len(item_ids), 60)]

    total_deposit = 0
    total_price = 0
    total_rooms = len(item_ids)
    for chunk in item_id_chunks:
        room_parameters = '&item_ids='.join([''] + [str(item_id)
                                                    for item_id in chunk])

        url = urljoin(base_url, ''.join([base_parameter, room_parameters]))

        request = Request(url)
        response = urlopen(request)

        data = json.loads(response.read())
        items = data['items']

        for item in items:
            total_deposit += item['item']['deposit']
            total_price += item['item']['rent']

    average_deposit = total_deposit / total_rooms

    average_price = total_price / total_rooms

    return average_deposit, average_price


def insert_zigbang_price(dabang_id, latitude, longitude):
    if not latitude or longitude:
        pass

    average = crawl_zigbang(latitude, longitude)

    deposit = average[0]
    price = average[1]

    station = Station.objects.get(dabang_id=dabang_id)
    price_object = Price.objects.create(
        station=station, deposit=deposit,
        price=price, source=Price.SOURCE_ZIGBANG)
    print(str(dabang_id) + ' ' + str(price_object.station.name) + ' '
          + str(price_object.deposit) + '/' + str(price_object.price) + ' '
          + str(price_object.get_source_display()))

    return (price_object.station.name,
            price_object.deposit,
            price_object.price)
