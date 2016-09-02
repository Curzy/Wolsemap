from django.db import models
# Create your models here.

class Line(models.Model):
    lines = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.lines

class Station(models.Model):
    station_id = models.IntegerField(unique=True)
    station_name = models.CharField(max_length=30, unique=True)
    station_lines = models.ManyToManyField(Line)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        info = str(self.station_id) + ' ' + str(self.station_name) + ' ' + str(self.station_lines.all())
        return info


class Price(models.Model):
    station = models.ForeignKey(Station, related_name='price_hitory')
    deposit = models.IntegerField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        info = str(self.station.station_id) + ' ' + str(self.station.station_name) + ' ' + str(self.deposit) + '/' + str(self.price) + ' ' + str(self.created_at)
        return info

