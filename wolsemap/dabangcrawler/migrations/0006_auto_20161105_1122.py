# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dabangcrawler', '0005_auto_20161105_1109'),
    ]

    operations = [
        migrations.RenameField(
            model_name='station',
            old_name='station_lines',
            new_name='line',
        ),
        migrations.RenameField(
            model_name='station',
            old_name='station_name',
            new_name='name',
        ),
    ]
