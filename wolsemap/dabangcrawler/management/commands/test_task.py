__author__ = 'Curzy'

from django.core.management import BaseCommand
from dabangcrawler.tasks import preset_subway_lines, insert_stations, insert_price
from concurrent.futures import ThreadPoolExecutor, as_completed


class Command(BaseCommand):

    def handle(self, *args, **options):
        preset_subway_lines()
        insert_stations(1, 789)

        with ThreadPoolExecutor(max_workers=15) as executor:
            #다방 역 인덱스 1 - 788 까지 돌림
            future_to_id = {executor.submit(insert_price, station_id): station_id for station_id in range(1, 789)}
