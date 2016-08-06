__author__ = 'Curzy'

import re

def sort_by_line (file_object) :


    result = {}

    while True:
        text = file_object.readline()
        if not text: break
        info = text.split()
        station_name = info[1]

        pattern = re.compile('[0-9]?[가-힣]+') #역 호선 거르기
        station_line = pattern.findall(str(info[2:-1]))
        station_price = info[-1]

        for i in station_line :
            if i in result :
                result[i].append((station_name, station_price))
            else :
                result[i] = [(station_name, station_price)]

    return result

def write (file_object, sorted_dict) :

    filtering_line = ('1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선', '9호선', '분당선', '신분당선', '경의선', '중앙선')

    for i in filtering_line :
        data = i + str(sorted_dict.get(i))
        file_object.write(data + '\n')

if __name__ == "__main__" :
    read_f = open("MetroRentalFee.txt", 'r')

    sorted = sort_by_line(read_f)


    read_f.close()

    write_f = open("SortedMetro.txt", 'w')

    write (write_f, sorted)

    write_f.close()

