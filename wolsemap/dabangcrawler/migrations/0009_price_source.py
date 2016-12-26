# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dabangcrawler', '0008_auto_20161226_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='source',
            field=models.SmallIntegerField(default=1, choices=[(1, 'DABANG'), (2, 'ZIGBANG')]),
            preserve_default=False,
        ),
    ]
