# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dabangcrawler', '0004_auto_20161022_1816'),
    ]

    operations = [
        migrations.RenameField(
            model_name='station',
            old_name='station_id',
            new_name='dabang_id',
        ),
    ]
