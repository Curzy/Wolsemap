# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from celery import shared_task

from django.conf import settings
from .models import Station, Price
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request, json
import zlib

PROJECT_PATH = settings.PROJECT_PATH


def crawl_dabang(station_id, page_number):

    #Config

    #수도권 지하철 호선
    SUBWAY_LINES = ('1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선', '9호선', '분당선', '신분당선', '경의선', '중앙선', '공항철도', '용인에버라인')

    #방 크기 범위, 제곱미터 단위
    ROOMSIZE_MIN = 16
    ROOMSIZE_MAX = 33
    #보증금 - 만원단위
    DEPOSIT_MIN = 0
    DEPOSIT_MAX = 5000

    #월세 - 만원단위
    PRICE_MIN = 10
    PRICE_MAX = 999999

    #방 종류 list로 / 0: 원룸, 1: 1.5룸, 2: 투룸, 3: 쓰리룸, 4: 오피스텔, 5: 아파트
    ROOMTYPE = [0]


    """dabang에서 역 하나, 페이지를 지정하여 JSON데이터를 긁어온다. 역에 매물이 있고, 수도권 역일 경우엔 리턴한다"""

    #검색조건 room-type 0 = 월세만, deposit-range 보증금, price-range 범위, room-size 5평 - 10평 사이
    url = ('http://www.dabangapp.com/api/2/room/list/subway?'
               'filters={"room-type":' + str(ROOMTYPE) +
               ',"room-size":['+ str(ROOMSIZE_MIN) +
               ','+ str(ROOMSIZE_MAX) + '],"deposit-range":['+ str(DEPOSIT_MIN) +
               ',' + str(DEPOSIT_MAX) + '],"price-range":[' + str(PRICE_MIN) + ',' +
               str(PRICE_MAX)+ ']}&id=' + str(station_id) + '&page=' +
               str(page_number)
    )
    request = urllib.request.Request(url, headers={'Accept-Encoding': 'gzip'})
    response = urllib.request.urlopen(request)
    dump = zlib.decompress(response.read(), 47).decode('utf-8')
    station_data = json.loads(dump)
    response.close()

    total_room = station_data['total']
    subway_line = station_data['subway']['line']
    #수도권 호선인지 검사 #방이 없는 역일 경우 넘김
    if not subway_line:
        return False
    elif subway_line[0] not in SUBWAY_LINES:
        return False
    elif total_room == 0 :
        return False
    else :
        #방이 있으나 수도권 역이 아님
        return station_data


def averaging(station_info):
    """각 역의 검색 결과에서 방들의 보증금과 월세를 평균낸다"""
    #총 보증금, 월세, 방 수
    total_deposit = 0
    total_price = 0
    total_rooms = 0

    station_name = station_info['subway']['name']
    subway_line = station_info['subway']['line']

    while True :
        for room in station_info['rooms'] :
            #"price_info": [[1000,40]]

            room_deposit = room['price_info'][0][0]
            total_deposit += room_deposit #방별 보증금을 합함

            room_price = room['price_info'][0][1]
            total_price += room_price

            total_rooms += 1
        #첫 페이지 값 계산 후, 다음 페이지가 있는지 체크, 없다면 break후 반복문 탈출, 있다면 다음

        has_more = station_info['has-more']
        if has_more :
            station_info = crawl_dabang(station_info['subway']['id'], station_info['next-page'])
        else :
            break

    average_deposit = total_deposit / total_rooms
    average_deposit = int(round(average_deposit, -2))  #보증금은 10의자리로 반올림

    average_price = total_price / total_rooms
    average_price = int(round(average_price, -1))  #월세는 1의자리로 반올림

    return station_name, subway_line, average_deposit, average_price



@shared_task
def insert_price(station_id):
    crawled = crawl_dabang(station_id, page_number=1)
    if crawled :
        average = averaging(crawled)
        deposit = average[2]
        price = average[3]
        station = Station.objects.get(station_id=station_id)
        price_object = Price.objects.create(station=station, deposit=deposit, price=price)
        print(str(station_id) + ' ' + str(price_object.station.station_name) + ' ' + str(price_object.deposit) + '/' + str(price_object.price))
        return price_object.station.station_name, price_object.deposit, price_object.price



@shared_task
def insert_prices(station_id_start, station_id_end):

    recent_price_dict = {}

    with ThreadPoolExecutor(max_workers=15) as executor:
        future_to_id = {executor.submit(insert_price, station_id): station_id for station_id in range(station_id_start, station_id_end)}
        for future in as_completed(future_to_id):
            station_id = future_to_id[future]
            try:
                station_info = future.result()
            except Exception as e:
                print('station id : %d generated an exception: %s' % (station_id, e))
            if station_info :
                recent_price_dict[station_id] = station_info

    with open(os.path.join(PROJECT_PATH, 'dabangcrawler/maps/Seoul_subway_linemap_ko.svg'), 'r') as original_map_f:
        with open(os.path.join(PROJECT_PATH, 'dabangcrawler/static/svg/price_inserted_subway_linemap.svg'), 'w') as subway_price_map_f:
            price_to_map(original_map_f, subway_price_map_f, recent_price_dict)

@shared_task
def price_to_map(original_subway_map, subway_price_map, recent_price_dict):
    original_map = original_subway_map.read()

    for station_id in list(recent_price_dict.keys()):
        station_info = recent_price_dict[station_id]

        station_name = station_info[0]
        station_name_without_yeok = station_name[0:-1]

        station_price = str(station_info[1]) + "/" + str(station_info[2])

        name_with_price = station_name_without_yeok + ' ' + station_price

        original_map = original_map.replace('>' + station_name_without_yeok + '<', '>' + name_with_price + '<')

    subway_price_map.write(original_map)

    return True

