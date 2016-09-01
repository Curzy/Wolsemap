# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lines', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deposit', models.IntegerField()),
                ('price', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('station_id', models.IntegerField()),
                ('station_name', models.CharField(max_length=30)),
                ('station_lines', models.ManyToManyField(to='dabangcrawler.Line')),
            ],
        ),
        migrations.AddField(
            model_name='price',
            name='station_id',
            field=models.ForeignKey(to='dabangcrawler.Station'),
        ),
    ]
