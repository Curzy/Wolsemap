# -*- coding: utf-8 -*-

import urllib.request
import json
import codecs


def crawl_dabang(station_id):
    request = 'http://www.dabangapp.com/api/2/room/list/subway?page=1&filters=%7B%22deposit-range%22%3A%5B0%2C999999%5D%2C%22price-range%22%3A%5B0%2C999999%5D%2C%22room-type%22%3A%5B0%5D%2C%22location%22%3A%5B%5B126.83457005023877%2C37.552415613220674%5D%2C%5B126.87572586536328%2C37.56966333742125%5D%5D%7D&id=' + str(station_id) + '&_=1454418074181'

    response = urllib.request.urlopen(request)

    reader = codecs.getreader("utf-8")
    obj = json.load(reader(response))
    response.close()
    return obj

def filter(json_object):

    filtering_line = ('1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선', '9호선', '분당선', '신분당선', '경의선', '중앙선')

    station_name = json_object['subway']['name']
    subway_line = json_object['subway']['line']

    #print(subway_line)

    if subway_line[0] in filtering_line:
        print(station_name)
        print(subway_line)
        #for i in json_object['rooms'] :
            #print(i['price_info'])
    return None

for i in range(1, 100):
    crawled = crawl_dabang(i)
    filter(crawled)