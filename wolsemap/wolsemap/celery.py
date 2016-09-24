from __future__ import absolute_import
from celery import Celery
from django.conf import settings

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wolsemap.settings')

app = Celery('wolsemap')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == '__main__':
    app.start()