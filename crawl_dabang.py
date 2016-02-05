# -*- coding: utf-8 -*-

import urllib.request
import json
import codecs
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def crawl_dabang(station_id):

    request = 'http://www.dabangapp.com/api/2/room/list/subway?page=1&id=' + str(station_id)

    response = urllib.request.urlopen(request)

    reader = codecs.getreader("utf-8")
    obj = json.load(reader(response))
    response.close()
    return obj

def filter_by_line(json_object): #현재 검색하는 역이 서울을 지나는 지하철이고 방이 있는 역인지

    filtering_line = ('1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선', '9호선', '분당선', '신분당선', '경의선', '중앙선')

    total_room = json_object['total']



    if total_room != 0: #방이 없는 역을 제외 / id=412 같은 경우 아예 정보가 없음 이거 무슨 데이터지 ??

        station_name = json_object['subway']['name']
        subway_line = json_object['subway']['line']

        if subway_line[0] in filtering_line :
            return station_name, subway_line
        else :
            return False
    else :
        return False

def averaging(json_object) : #각 역의 검색 결과에서 방들의 보증금과 월세를 평균냄
    total_deposit = 0

    total_price = 0

    counter = 0

    for i in json_object['rooms'] :
        room_deposit = i['price_info'][0][0]
        total_deposit += room_deposit #방별 보증금을 합함

        room_price = i['price_info'][0][1]
        total_price += room_price

        counter += 1


    average_deposit = total_deposit / counter
    average_deposit = int(round(average_deposit, -1)) # 보증금은 10의자리로 반올림

    average_price = total_price / counter
    average_price = round(average_price) #월세는 1의자리로 반올림

    return average_deposit, average_price

def write(iter, file_object) : #결과를 txt파일에 저장하는 함수

    crawled = crawl_dabang(iter)
    filtered = filter_by_line(crawled)
    if filtered != False :
        average = averaging(crawled)
        data = str(iter) + " " + str(filtered[0]) + " " + str(filtered[1]) + " " + str(average[0]) + "/" + str(average[1])
        print(data)
        file_object.write(data + "\n")

if __name__ == "__main__" :

    start = time.time()

    f = open("MetroRentalFee.txt", 'w') #역, 호선, 보증금 월세를 저장하기 위한 파일 오픈

    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(1, 789):
            executor.submit(write, i, f)

    f.close()

    duration = time.time() - start
    print(duration)





