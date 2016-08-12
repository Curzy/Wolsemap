__author__ = 'Curzy'

import urllib.request
import json
import codecs
import time
from concurrent.futures import ThreadPoolExecutor

filtering_line = ('1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선', '9호선', '분당선', '신분당선', '경의선', '중앙선')

def main():
    start = time.time()

    with open("MetroRentalFee.txt", 'w') as station_price_list_f:
        with ThreadPoolExecutor(max_workers=10) as executor:
            #다방 역 인덱스 1 - 788 까지 돌림
            for station_id in range(1, 789):
                executor.submit(record_station_info, station_id, station_price_list_f)


    with open("MetroRentalFee.txt", 'r') as station_price_list_f:
        with open("Seoul_subway_linemap_ko.svg", 'r') as original_map_f:
            with open("price_inserted_subway_linemap.svg", 'w') as subway_price_map_f:
                insert_price(station_price_list_f, original_map_f, subway_price_map_f)



    duration = time.time() - start
    print(duration)


def record_station_info(station_id, file_object) :
    """역 이름, 노선, 평균 보증금, 평균 월세를 저장한다."""

    #station_id 에 해당하는 역 인덱스의 페이지 1번을 읽어 시작
    crawled = crawl_dabang(station_id, 1)
    if crawled :
        average = averaging(crawled)
        data = str(station_id) + " " + str(average[0]) + " " + str(average[1]) + " " + str(average[2]) + "/" + str(average[3])
        print(data)
        file_object.write(data + "\n")


def crawl_dabang(station_id, page_number):
    """dabang에서 역 하나, 페이지를 지정하여 JSON데이터를 긁어온다. 역에 매물이 있고, 수도권 역일 경우엔 리턴한다"""
    request = 'http://www.dabangapp.com/api/2/room/list/subway?filters={"room-type":[0],"room-size":[16,33],"deposit-range":[0,5000],"price-range":[10,999999]}&id=' + str(station_id) + '&page=' + str(page_number) #검색조건 room-type 0 = 월세만, deposit-range 보증금, price-range 범위, room-size 5평 - 10평 사이

    response = urllib.request.urlopen(request)

    reader = codecs.getreader("utf-8")

    station_data = json.load(reader(response))

    response.close()

    total_room = station_data['total']
    subway_line = station_data['subway']['line']
    #수도권 호선인지 검사 #방이 없는 역일 경우 넘김
    if subway_line[0] not in filtering_line :
        return False
    elif total_room == 0 :
        return False
    else :
        #방이 있으나 수도권 역이 아님
        return station_data

def averaging(station_info) :
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
    average_deposit = int(round(average_deposit, -2)) # 보증금은 10의자리로 반올림

    average_price = total_price / total_rooms
    average_price = int(round(average_price, -1)) #월세는 1의자리로 반올림

    return station_name, subway_line, average_deposit, average_price


def insert_price (station_price_list, original_subway_map, subway_price_map) :
    """역별로 가공된 데이터는 """
    original_map = original_subway_map.read()

    while True:
        #각 역별로 read한 자료는 _data 그중 내가 원하는 보증금과 가격의 정보만을 뽑을 수 있도록 하는 변수는 _info
        station_data  = station_price_list.readline()
        if not station_data: break
        station_info = station_data.split()
        station_name = station_info[1]
        station_name_without_yeok = station_name[0:-1]

        station_price = station_info[-1]

        name_with_price = station_name_without_yeok + ' ' + station_price

        print (name_with_price)
        original_map = original_map.replace('>' + station_name_without_yeok + '<', '>' + name_with_price + '<')
        #원본 svg지도 파일에 >신길< 이런식으로 저장이 되어 있는데 그중 역 이름 부분을 역 + 가격 텍스트로 치환함

    subway_price_map.write(original_map)

    return True



if __name__ == "__main__" :
    main()

