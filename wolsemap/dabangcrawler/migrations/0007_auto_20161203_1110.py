# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dabangcrawler', '0006_auto_20161105_1122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='line',
            old_name='lines',
            new_name='name',
        ),
    ]
