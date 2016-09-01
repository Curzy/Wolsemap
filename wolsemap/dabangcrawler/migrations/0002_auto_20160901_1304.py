# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dabangcrawler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 9, 1, 13, 4, 21, 708848, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 1, 13, 4, 24, 60191, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='station',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 9, 1, 13, 4, 28, 20418, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='station',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 1, 13, 4, 30, 155784, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='line',
            name='lines',
            field=models.CharField(unique=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='price',
            name='station_id',
            field=models.ForeignKey(to='dabangcrawler.Station', related_name='price_hitory'),
        ),
        migrations.AlterField(
            model_name='station',
            name='station_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='station_name',
            field=models.CharField(unique=True, max_length=30),
        ),
    ]
