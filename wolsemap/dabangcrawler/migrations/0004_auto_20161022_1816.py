# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dabangcrawler', '0003_auto_20160901_1610'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='price',
            options={'get_latest_by': 'created_at'},
        ),
        migrations.AlterField(
            model_name='price',
            name='station',
            field=models.ForeignKey(related_name='price_history', to='dabangcrawler.Station'),
        ),
    ]
