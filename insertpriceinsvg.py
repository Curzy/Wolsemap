__author__ = 'Curzy'


def insert_price (read_file_object, svg_file_object, write_file_object) :

    svg = svg_file_object.read()

    while True:
        text = read_file_object.readline()
        if not text: break
        info = text.split()
        station_name = info[1]
        station_name_without_yeok = station_name[0:-1]

        station_price = info[-1]

        name_with_price = station_name_without_yeok + ' ' + station_price

        print (name_with_price)
        svg = svg.replace(station_name_without_yeok, name_with_price)

    write_file_object.write(svg)

    return True

if __name__ == "__main__" :

    with open("MetroRentalFee.txt", 'r') as read_f:
        with open("Seoul_subway_linemap_ko.svg", 'r') as svg_f:
            with open("price_inserted_subway_linemap.svg", 'w') as write_f:
                insert_price(read_f, svg_f, write_f)


