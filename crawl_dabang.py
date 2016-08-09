__author__ = 'Curzy'

import urllib.request
import json
import codecs
import time
from concurrent.futures import ThreadPoolExecutor

filtering_line = ('1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선', '9호선', '분당선', '신분당선', '경의선', '중앙선')

def main():
    start = time.time()

    with open("MetroRentalFee.txt", 'w') as f:
        with ThreadPoolExecutor(max_workers=10) as executor:
            for i in range(1, 789): #다방 역 인덱스 1 - 788 까지 돌림
                executor.submit(record_station_info, i, f)

    duration = time.time() - start
    print(duration)

def record_station_info(station_id, file_object) :
    """역 이름, 노선, 평균 보증금, 평균 월세를 저장한다."""

    crawled = crawl_dabang(station_id, 1) #station_id 에 해당하는 역 인덱스의 페이지 1번을 읽어 시작
    if crawled :
        average = averaging(crawled)
        data = str(station_id) + " " + str(average[0]) + " " + str(average[1]) + " " + str(average[2]) + "/" + str(average[3])
        print(data)
        file_object.write(data + "\n")


def crawl_dabang(station_id, page_number):
    """dabang에서 역 하나, 페이지를 지정하여 JSON데이터를 긁어온다. 역에 매물이 있고, 수도권 역일 경우엔 리턴한다"""
    request = 'http://www.dabangapp.com/api/2/room/list/subway?filters={"room-type":[0],"room-size":[16,33],"deposit-range":[0,5000],"price-range":[10,999999]}&id=' + str(station_id) + '&page=' + str(page_number) #검색조건 room-type 0 = 월세만, deposit-range 보증금, price-range 범위, room-size 5평 - 10평 사이

    response = urllib.request.urlopen(request)

    reader = codecs.getreader("utf-8") #유니코드로 긁어오기

    station_info = json.load(reader(response))

    response.close()

    total_room = station_info['total']
    subway_line = station_info['subway']['line']

    if subway_line[0] not in filtering_line : #수도권 호선인지 검사 #방이 없는 역일 경우 넘김
        return False
    elif total_room == 0 :
        return False
    else :
        return station_info #방이 있으나 수도권 역이 아님

def averaging(station_info) :
    """#각 역의 검색 결과에서 방들의 보증금과 월세를 평균낸다"""
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
    average_deposit = int(round(average_deposit, -2)) # 보증금은 10의자리로 반올림

    average_price = total_price / total_rooms
    average_price = int(round(average_price, -1)) #월세는 1의자리로 반올림

    return station_name, subway_line, average_deposit, average_price

if __name__ == "__main__" :
    main()

