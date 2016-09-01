from django.db import models
from django.utils import timezone
# Create your models here.

class Line(models.Model):
    lines = models.CharField(max_length=20)

    def __str__(self):
        return self.lines

class Station(models.Model):
    station_id = models.IntegerField()
    station_name = models.CharField(max_length=30)
    station_lines = models.ManyToManyField(Line)

    def __str__(self):
        info = str(self.station_id), str(self.station_name), str(self.station_lines.all())
        return info

class Price(models.Model):
    station_id = models.ForeignKey(Station)
    deposit = models.IntegerField()
    price = models.IntegerField()
    timestamp = models.DateTimeField()

