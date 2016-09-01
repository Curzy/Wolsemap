# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dabangcrawler', '0002_auto_20160901_1304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='price',
            old_name='station_id',
            new_name='station',
        ),
        migrations.RemoveField(
            model_name='price',
            name='timestamp',
        ),
    ]
