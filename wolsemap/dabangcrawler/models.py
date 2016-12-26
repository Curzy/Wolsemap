from django.db import models


class Line(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Station(models.Model):
    dabang_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=30, unique=True)
    line = models.ManyToManyField(Line)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        info = ' '.join(
            [str(self.dabang_id), str(self.name), str(self.line.all())]
        )
        return info


class Price(models.Model):
    SOURCE_DABANG = 1
    SOURCE_ZIGBANG = 2

    SOURCE_CHOICES = (
        (SOURCE_DABANG, 'DABANG'),
        (SOURCE_ZIGBANG, 'ZIGBANG')
    )

    class Meta:
        get_latest_by = 'created_at'

    station = models.ForeignKey(Station, related_name='price_history')
    deposit = models.IntegerField()
    price = models.IntegerField()
    source = models.SmallIntegerField(choices=SOURCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        info = str(self.station.dabang_id) + ' ' + \
            str(self.station.name) + ' ' + \
            str(self.deposit) + '/' + \
            str(self.price) + ' ' + \
            str(self.created_at)
        return info
