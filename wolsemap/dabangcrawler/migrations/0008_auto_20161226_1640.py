# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dabangcrawler', '0007_auto_20161203_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='station',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
